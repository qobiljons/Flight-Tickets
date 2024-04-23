import requests
import os


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.sheety_prices_api = os.environ["sheety_prices_api"]
        self.sheety_users_api = os.environ["sheety_users_api"]

    def get_destination_data(self):
        response = requests.get(self.sheety_prices_api)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_iata_codes(self):
        for data in self.destination_data:
            update_query = {"price": {"iataCode": data["iataCode"]}}
            response = requests.put(url=f"{self.sheety_prices_api}{data['id']}", json=update_query)
            response.raise_for_status()

    def update_prices(self):
        for data in self.destination_data:

            update_query = {"price": {"lowestPrice": data["lowestPrice"]}}
            response = requests.put(url=f"{self.sheety_prices_api}{data['id']}", json=update_query)
            response.raise_for_status()

    def get_users(self):
        response = requests.get(url=self.sheety_users_api)
        user_emails = response.json()["users"]
        return user_emails


db = DataManager()

print(db.get_users())

