import os
import argparse
from twilio.rest import Client
import geocoder
import gpsd


#יצא לי תוצאות לא ככ מדויקות
def get_location_auto():
    g = geocoder.ip('me')
    if g.ok and g.latlng:
        return g.latlng  # מחזיר [lat, lng]
    return None
def get_location_gps():
    try:
        gpsd.connect()  # התחברות ל־gpsd :contentReference[oaicite:1]{index=1}
        packet = gpsd.get_current()  # בקשת המיקום הנוכחי :contentReference[oaicite:2]{index=2}
        lat, lng = packet.lat, packet.lon
        if lat is not None and lng is not None:
            return [lat, lng]
    except Exception:
        pass
    return None
parser = argparse.ArgumentParser(description="Send emergency SMS with automatic or manual location")
parser.add_argument('--lat', type=float, help='Latitude (manual override)')
parser.add_argument('--lng', type=float, help='Longitude (manual override)')
args = parser.parse_args()

if args.lat is not None and args.lng is not None:
    lat, lng = args.lat, args.lng
else:
    gps_loc = get_location_gps()
    if gps_loc:
        lat, lng = gps_loc
        print(f"Using GPS location: {lat}, {lng}")
    else:
        ip_loc = get_location_auto()
        if ip_loc:
            lat, lng = ip_loc
            print(f"Using IP-based location: {lat}, {lng}")
        else:
            # קלט ידני סופי
            lat = float(input("Enter latitude manually: "))
            lng = float(input("Enter longitude manually: "))

# if args.lat is not None and args.lng is not None:
#     lat, lng = args.lat, args.lng
# else:
#     auto = get_location_auto()
#     if auto:
#         lat, lng = auto
#         print(f"Using automatic location: {lat}, {lng}")
#     else:
#         # קלט ידני מהמשתמש
#         lat = float(input("Enter latitude manually: "))
#         lng = float(input("Enter longitude manually: "))
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
        f"Location: https://maps.google.com/?q={lat},{lng}"
)
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


    #לסדר את המיקום שיהיה מדויק לבדוק האם הקוד מתייחס לGPS
    #להקפיץ שאלה למשתמש האם זה המיקום שלך ואם לא הכנס ידנית