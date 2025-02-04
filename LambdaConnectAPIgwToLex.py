import json
import boto3

# Tạo client Lex Runtime
lex_client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    # Debug: Log toàn bộ event nhận được từ API Gateway
    print("Received event:", json.dumps(event, indent=2))

    # Lấy tin nhắn người dùng từ body của yêu cầu
    try:
        body = json.loads(event['body'])
        user_message = body.get('message', '')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON or missing message'})
        }

    if not user_message:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Message is required'})
        }

    try:
        # Thông tin của Bot Lex
        bot_id = '8M5KCX2WDN'  # Bot ID của bạn
        bot_alias_id = 'TSTALIASID'  # Bot Alias ID của bạn
        locale_id = 'en_US'  # Locale của bot (ví dụ en_US)
        session_id = str(uuid.uuid4())

        # Gửi yêu cầu tới Lex
        response = lex_client.recognize_text(
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId=locale_id,
            sessionId=session_id,
            text=user_message
        )

        # Xử lý phản hồi từ Lex
        messages = response.get('messages', [])
        if messages:
            bot_reply = messages[0].get('content', 'Sorry, I didn’t understand that.')
        else:
            bot_reply = 'Sorry, something went wrong.'

        # Trả về phản hồi cho API Gateway
        return {
            'statusCode': 200,
            'body': json.dumps({'message': bot_reply})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
