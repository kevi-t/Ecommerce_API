# orders/services.py
import africastalking
import re
from django.conf import settings


username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_API_KEY
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def format_phone_number(phone_number):
    if phone_number is None or phone_number.strip() == "":
        print("Error: Received an empty or None phone number")
        raise ValueError("Phone number cannot be empty")

    phone_number = phone_number.strip()  # Remove spaces
    print(f"Debug: Raw phone number received - {phone_number}")

    # Validate phone number format (must start with + or 0, and be 9-15 digits long)
    if not re.match(r"^\+?\d{9,15}$", phone_number):
        print(f"Error: Invalid phone number format - {phone_number}")
        raise ValueError(f"Invalid phone number: {phone_number}")

    # Convert 0792526394 → +254792526394
    if phone_number.startswith("0"):
        formatted = "+254" + phone_number[1:]
    elif phone_number.startswith("+"):
        formatted = phone_number
    else:
        raise ValueError(f"Invalid phone number format: {phone_number}")
    
    print(f"Debug: Formatted phone number - {formatted}")
    return formatted
     

def send_sms(phone_number, message):
    try:
        formatted_number = format_phone_number(phone_number)
        phone_list = [formatted_number]
        print(f"Debug: Sending SMS to {phone_list}")
        response = sms.send(message, phone_list)
        print(f"SMS sent successfully: {response}")
        return response
    except Exception as e:
        print(f"An error occurred while sending SMS: {e}")
        return None