import boto3  # Thêm import boto3 để kết nối với DynamoDB
import json
import datetime
import time

def validate(slots):
    valid_cities = ['hanoi','mumbai','tokyo','paris','seoul']
    
    if not slots['Location']:
        print("Inside Empty Location")
        return {
        'isValid': False,
        'violatedSlot': 'Location'
        }        
        
    if slots['Location']['value']['originalValue'].lower() not in valid_cities:
        print("Not Valide location")
        return {
        'isValid': False,
        'violatedSlot': 'Location',
        'message': 'We currently support only {} as a valid destination.'.format(", ".join(valid_cities))
        }
        
    if not slots['CheckInDate']:
        return {
        'isValid': False,
        'violatedSlot': 'CheckInDate',
    }
        
    if not slots['Nights']:
        return {
        'isValid': False,
        'violatedSlot': 'Nights'
    }
        
    if not slots['RoomType']:
        return {
        'isValid': False,
        'violatedSlot': 'RoomType'
    }
    
    if not slots['Email']:
        return {
        'isValid': False,
        'violatedSlot': 'Email'
        }

    return {'isValid': True}
    
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')  # Kết nối với DynamoDB
    table_name = "BookingHotel"           # Tên bảng DynamoDB
    table = dynamodb.Table(table_name)
    
    # print(event)
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            if 'message' in validation_result:
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": validation_result['message']
                    }
                ]
               } 
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                    }
                }
               } 
            return response
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name':intent,
                    'slots': slots
                }
            }
        }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        # Lấy thông tin từ slots
        reservation_id = f"res_{int(time.time())}"  # Tạo ID duy nhất
        location = slots['Location']['value']['originalValue']
        check_in_date = slots['CheckInDate']['value']['originalValue']
        nights = int(slots['Nights']['value']['interpretedValue'])
        room_type = slots['RoomType']['value']['originalValue']
        email = slots['Email']['value']['originalValue']
        
        # Tạo đối tượng lưu trữ
        item = {
            "ReservationID": reservation_id,
            "Location": location,
            "CheckInDate": check_in_date,
            "Nights": nights,
            "RoomType": room_type,
            "Timestamp": int(time.time()),
            "Email": email
        }

        # Lưu vào DynamoDB
        try:
            table.put_item(Item=item)
            print(f"Reservation saved: {item}")
        except Exception as e:
            print(f"Error saving reservation: {e}")

        # Trả về phản hồi
        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Thanks, I have placed your reservation"
            }
        ]
    }
            
        return response
