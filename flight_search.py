import requests
import datetime as dt
from flight_data import FlightData


TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
date_format = '%d/%m/%Y'
ORIGIN_CITY_IATA = 'LON'


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

    def search_flights(self, destination_city_code):
        tmr_date = dt.datetime.today() + dt.timedelta(days=1)
        max_date = dt.datetime.today() + dt.timedelta(days=180)
        headers = {
            'apikey': self.tequila_api
        }
        parameters = {
            'fly_from': ORIGIN_CITY_IATA,
            'fly_to': destination_city_code,
            'date_from': tmr_date.strftime(date_format),
            'date_to': max_date.strftime(date_format),
            'max_stopovers': 0,
            'curr': 'GBP',
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            "one-for-city": 1
        }

        response = requests.get(
            url=f'{TEQUILA_ENDPOINT}/v2/search',
            headers=headers,
            params=parameters
        )
        response.raise_for_status()

        try:
            data = response.json()['data'][0]
        except IndexError:
            parameters['max_stopovers'] = 1
            response = requests.get(
                url=f'{TEQUILA_ENDPOINT}/v2/search',
                headers=headers,
                params=parameters
            )
            response.raise_for_status()
            print(response.json())
            if len(response.json()['data']) > 0:
                data = response.json()['data'][0]

                flight_data = FlightData(price=data['price'], city_from=data['cityFrom'], fly_from=data['flyFrom'],
                                         city_to=data['cityTo'], fly_to=data['flyTo'],
                                         leave_date=data["route"][0]["local_departure"].split("T")[0],
                                         return_date=data["route"][1]["local_departure"].split("T")[0],
                                         stop_overs=1, via_city=data["route"][0]["cityTo"])
                return flight_data
            else:
                return None

        else:
            flight_data = FlightData(price=data['price'], city_from=data['cityFrom'], fly_from=data['flyFrom'],
                                     city_to=data['cityTo'], fly_to=data['flyTo'],
                                     leave_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][1]["local_departure"].split("T")[0],
                                     )
            return flight_data


