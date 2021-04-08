class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, price, city_from, fly_from, city_to, fly_to,
                 leave_date, return_date, stop_overs=0, via_city=""):
        self.price = price
        self.departure_city_name = city_from
        self.departure_airport = fly_from
        self.arrival_city_name = city_to
        self.arrival_airport = fly_to
        self.outbound_date = leave_date
        self.inbound_date = return_date
        self.stop_overs = stop_overs
        self.via_city = via_city



