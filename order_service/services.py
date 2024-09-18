import africastalking

# Initialize Africa's Talking
username = 'your_sandbox_username'
api_key = 'your_api_key'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_sms(phone_number, message):
    response = sms.send(message, [phone_number])
    return response