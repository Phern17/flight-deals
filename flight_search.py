import requests
import datetime as dt
from flight_data import FlightData


TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
date_format = '%d/%m/%Y'


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, tequila_api):
        self.tequila_api = tequila_api

    def get_city_code(self, city_name):
        parameters = {
            'apikey': self.tequila_api,
            'term': city_name,
            'locale': "en-US",
            'location_types': 'city',
            'limit': "1"
        }
        response = requests.get(url=f'{TEQUILA_ENDPOINT}/locations/query', params=parameters)
        response.raise_for_status()
        data = response.json()['locations'][0]['code']
        return data

    def search_flights(self, destination_city_code, aim_price):
        tmr_date = dt.datetime.today() + dt.timedelta(days=1)
        max_date = dt.datetime.today() + dt.timedelta(days=180)
        parameters = {
            'apikey': self.tequila_api,
            'fly_from': 'LON',
            'fly_to': destination_city_code,
            'date_from': tmr_date.strftime(date_format),
            'date_to': max_date.strftime(date_format),
            'price_to': aim_price,
            'limit': 1,
            'max_stopovers': 0,
            'curr': 'GBP',
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            "one-for-city": 1
        }

        response = requests.get(url=f'{TEQUILA_ENDPOINT}/v2/search', params=parameters)
        response.raise_for_status()

        try:
            data = response.json()['data'][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data_formatter = FlightData()
        return flight_data_formatter.format_data(data)


