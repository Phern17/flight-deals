#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import os

TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_API = os.environ.get('TWILIO_API')
TEQUILA_API = os.environ.get('TEQUILA_API')
PW_GMAIL = os.environ.get("PW_GMAIL")

dm = DataManager()
sheet_data = dm.get_destination_data()
fs = FlightSearch(tequila_api=TEQUILA_API)

notification_mng = NotificationManager(TWILIO_SID, TWILIO_API, gmail_password=PW_GMAIL)

if sheet_data[0]['iataCode'] == "":
    for city in sheet_data:
        city['iataCode'] = fs.get_city_code(city['city'])

    dm.destination_data = sheet_data
    dm.update_destination_data()

for item in sheet_data:
    flight_data = fs.search_flights(item['iataCode'])

    if flight_data is None:
        pass

    if flight_data.price < item['lowestPrice']:
        users = dm.get_client_emails()
        emails = [item['email'] for item in users]

        msg = f'Low Price alert! Only £{flight_data.price} to fly from ' \
              f'{flight_data.departure_city_name}-{flight_data.departure_airport} ' \
              f'to {flight_data.arrival_city_name}-{flight_data.arrival_airport}, ' \
              f'from {flight_data.outbound_date} to {flight_data.inbound_date}'

        if flight_data.stop_overs > 0:
            msg += f'\nFlight has 1 stop over, via {flight_data.via_city}.'

        link = f'link = https://www.google.co.uk/flights?hl=en#flt=' \
               f'{flight_data.departure_airport}.' \
               f'{flight_data.arrival_airport}.' \
               f'{flight_data.outbound_date}*{flight_data.arrival_airport}.' \
               f'{flight_data.inbound_date}.{flight_data.departure_airport}'

        notification_mng.send_emails(emails=emails, message=msg, link=link)
