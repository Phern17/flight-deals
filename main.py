#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import os

TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_API = os.environ.get('TWILIO_API')
TEQUILA_API = os.environ.get('TEQUILA_API')

dm = DataManager()
sheet_data = dm.get_destination_data()
fs = FlightSearch(tequila_api=TEQUILA_API)

notification_mng = NotificationManager(TWILIO_SID, TWILIO_API)

if sheet_data[0]['iataCode'] == "":
    for city in sheet_data:
        city['iataCode'] = fs.get_city_code(city['city'])

    dm.destination_data = sheet_data
    dm.update_destination_data()

for item in sheet_data:
    print(type(item['lowestPrice']))
    msg = fs.search_flights(item['iataCode'], item['lowestPrice'])
    print(msg)
    if msg is not None:
        notification_mng.send_notification(message=msg)