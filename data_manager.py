import requests

SHEETY_ENDPOINT = "https://api.sheety.co/4c1e1a5d69d2d0a6ba11451485e9a07a/flightDeals/prices"


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):

        response = requests.get(url=SHEETY_ENDPOINT)
        response.raise_for_status()
        self.destination_data = response.json()['prices']
        return self.destination_data

    def update_destination_data(self):
        for item in self.destination_data:
            body = {
                'price': {
                    "iataCode": item['iataCode']
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{item['id']}", json=body)
