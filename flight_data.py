class FlightData:
    # This class is responsible for structuring the flight data.
    def format_data(self, data):
        price = data['price']
        departure_city_name = data['cityFrom']
        departure_airport_iata_code = data['flyFrom']
        arrival_city_name = data['cityTo']
        arrival_airport_iata_code = data['flyTo']
        outbound_date = data["route"][0]["local_departure"].split("T")[0]
        inbound_date = data["route"][1]["local_departure"].split("T")[0]
        msg = f'Only £{price} to fly from {departure_city_name}-{departure_airport_iata_code} ' \
              f'to {arrival_city_name}-{arrival_airport_iata_code}, from {outbound_date} to {inbound_date}'

        return msg