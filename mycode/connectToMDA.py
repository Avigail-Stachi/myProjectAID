import os
from twilio.rest import Client

# בדיקת מצב הפעלה: "production" או "development"
ENV = os.getenv("APP_ENV", "development")  # ברירת מחדל: פיתוח
#בסיום הפיתוח לשנות ל
#ENV = "production"
#או להגדיר משתנה סביבה


account_sid ='AC6b153d179999949c8d24dc9b08b3182e'
auth_token = '3013420d1c67594c5b6d9256940d9af8'
client = Client(account_sid, auth_token)

text = ("Test message from a first-aid mobile app development project.\n"
        "Emergency simulation: person unconscious.\n"
        "Location: https://maps.google.com/?q=31.7683,35.2137")
to_number = '+972527000101'  #SMS של מדא
from_number = '+17753708117' #המספר twilio שלי

# שליחת הודעה
if ENV == "production":
    message = client.messages.create(
        body=text,
        from_=from_number,
        to=to_number
    )
    print("Message sent successfully! SID:", message.sid)
else:
    print("Development mode – SMS was not sent.")
    print("Simulated message:")
    print(f"To: {to_number}\nBody:\n{text}")