import json
import boto3
import datetime

# Tạo SNS client
sns_client = boto3.client('sns')

# ARN của SNS Topic (Cần tạo SNS topic trong AWS Console)
SNS_TOPIC_ARN = 'arn:aws:sns:ap-southeast-2:361769598486:MyLabSNS'

def lambda_handler(event, context):
    # Lặp qua tất cả các bản ghi (records) trong DynamoDB Stream
    for record in event['Records']:
        # Kiểm tra sự kiện INSERT hoặc MODIFY (tùy vào yêu cầu của bạn)
        if record['eventName'] == 'INSERT' or record['eventName'] == 'MODIFY':
            # Lấy thông tin đặt phòng từ NewImage (khi có sự kiện INSERT hoặc MODIFY)
            new_image = record['dynamodb']['NewImage']
            
            # Lấy các trường thông tin đặt phòng
            location = new_image['Location']['S']
            checkin_date = new_image['CheckInDate']['S']
            nights = new_image['Nights']['N']
            room_type = new_image['RoomType']['S']
            user_email = new_image['Email']['S']  # Giả sử bạn lưu email của người dùng trong bảng

            # Tạo nội dung email
            message = f"""
            Hello,

            Thank you for booking with us. Here are your reservation details:

            - Location: {location}
            - Check-in Date: {checkin_date}
            - Nights: {nights}
            - Room Type: {room_type}

            We look forward to welcoming you!

            Best regards,
            Your Hotel Booking Service
            """

            # Gửi thông điệp qua SNS (email cho người dùng)
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject="Your Hotel Reservation Confirmation",
                MessageAttributes={
                    'Email': {
                        'DataType': 'String',
                        'StringValue': user_email
                    }
                }
            )
            print(f"Email sent to {user_email}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed successfully!')
    }
