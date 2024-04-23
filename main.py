from data_manager import DataManager
from flight_search import FlightSearch
import datetime as dt
from notification_manager import NotificationManager

ORIGIN_CITY_CODE = "LON"
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
message_sender = NotificationManager()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_iata_codes()

tomorrow = dt.datetime.now() + dt.timedelta(days=1)
six_months = dt.datetime.now() + dt.timedelta(days=180)

flights = []
for destination in sheet_data:
    flight_data = flight_search.check_flights(ORIGIN_CITY_CODE, destination["iataCode"], tomorrow, six_months)
    if flight_data is None:
        flights_with_stopovers = flight_search.check_flights(
            ORIGIN_CITY_CODE,
            destination["iataCode"],
            tomorrow,
            six_months)
    flights.append(flight_data)
data_manager.destination_data = sheet_data
data_manager.update_prices()


def find_the_cheapest(iterable):
    cheapest_price = iterable[0]
    minimum = iterable[0].price
    for item in iterable:
        if item is None:
            continue
        elif item.price < minimum:
            cheapest_price = item
            message = f"From {cheapest_price.origin_city} to {cheapest_price.destination_city}.\nPrice: ${cheapest_price.price}.\nUTC-TIME departure: {cheapest_price.out_date.split('T')[0]}.\nUTC-TIME arrival: {cheapest_price.return_date.split('T')[0]}"
            if item.stop_overs > 0:
                message += f"Flight has {cheapest_price.stop_overs} stopover via {cheapest_price.via_city}"
        return cheapest_price


result = find_the_cheapest(flights)
message = (f"From {result.origin_city}"
           f" to {result.destination_city}."
           f"\nPrice: ${result.price}."
           f"\nUTC-TIME departure: {result.out_date.split('T')[0]}."
           f"\nUTC-TIME arrival: {result.return_date.split('T')[0]}")

if result.stop_overs > 0:
    message += f"\n Flight has {result.stop_overs} stopover via {result.via_city}"

emails = data_manager.get_users()
for email in emails:
    send = message_sender.send_message(message, email["email"])

