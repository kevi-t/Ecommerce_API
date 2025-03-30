# orders/services.py
import africastalking
from django.conf import settings


username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_API_KEY
africastalking.initialize(username, api_key)
sms = africastalking.SMS

#Test program
response = sms.send("Test Message", ["+254792526394"])
print(response)

def send_sms(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print(f"SMS sent successfully: {response}")
        return response
    except Exception as e:
        print(f"An error occurred while sending SMS: {e}")
        return None