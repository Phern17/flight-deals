import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/4c1e1a5d69d2d0a6ba11451485e9a07a/flightDeals/prices"
SHEETY_USERS_ENDPOINT = 'https://api.sheety.co/4c1e1a5d69d2d0a6ba11451485e9a07a/flightDeals/users'


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.users = {}

    def get_destination_data(self):

        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        response.raise_for_status()
        self.destination_data = response.json()['prices']
        print(self.destination_data)
        return self.destination_data

    def update_destination_data(self):
        for item in self.destination_data:
            body = {
                'price': {
                    "iataCode": item['iataCode']
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{item['id']}", json=body)

    def get_client_emails(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT)
        response.raise_for_status()
        self.users = response.json()['users']
        print(self.users)
        return self.users


