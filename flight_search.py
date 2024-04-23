import requests
import os
from flight_data import FlightData

TEQUILA_API_KEY = os.environ["tequila_api_key"]
TEQUILA_ENDPOINT = os.environ["tequila_endpoint"]


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.response = None
        self.location_params = None
        self.params = None
        self.header = {
            "apikey": TEQUILA_API_KEY,
        }

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        self.location_params = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, params=self.location_params, headers=self.header)
        code = response.json()["locations"][0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, max_stopovers=0):
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": max_stopovers,
            "curr": "GBP",
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=self.header)
        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 2
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=self.header)
            try:
                data = response.json()["data"][0]
            except IndexError:
                print("No Flight Available")
                return None
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["cityFrom"],
                origin_airport=data["cityCodeFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["cityCodeTo"],
                out_date=data["utc_departure"],
                return_date=data["utc_arrival"],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["cityFrom"],
                origin_airport=data["cityCodeFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["cityCodeTo"],
                out_date=data["utc_departure"],
                return_date=data["utc_arrival"]
            )
            return flight_data


