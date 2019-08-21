import requests
from datetime import datetime, timedelta
import logging
import time


FROM = 0
TO = 1
WHEN = 2



QUERY_BASE = "https://apidojo-kayak-v1.p.rapidapi.com/flights/"
CREATE_SESSION_BASE = "create-session?"
POLL_BASE = "poll?"
CABIN = "cabin"
CURRENCY = "currency"
BAGS = "bags"
PASSENGERS =  "adults"
ORIGIN = "origin{}"
DESTINATION = "destination{}"
DATE = "departdate{}"
HEADERS = {"X-RapidAPI-Host": "apidojo-kayak-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "a07bbf8525msh0f978afda6b7faep16106djsn80681f0b3680"}

CODE_MAP = {"tel aviv": "TLV",
            "hanoi": "HAN",
            "rome": "ROM"}

log = logging.getLogger("main")

def city_to_port_code(city):
    if city not in CODE_MAP:
        raise KeyError("unknown airport code for the city {}".format(city))
    return CODE_MAP[city]


def date_to_query_fromat(date):
    return date.strftime("%Y-%m-%d")


def direction_to_query_params(num, origin, destination, date):
    return {ORIGIN.format(num): city_to_port_code(origin), DESTINATION.format(num): city_to_port_code(destination),
            DATE.format(num): date_to_query_fromat(date)}


def construct_query_params(origins, destinations, dates, passengers):

    # construct individual query components
    params = {CABIN: "e", BAGS: 0, CURRENCY: "USD", PASSENGERS: passengers}
    for i, flight in enumerate(zip(origins, destinations, dates)):
        params.update(direction_to_query_params(i + 1, flight[FROM], flight[TO], flight[WHEN]))

    return params


def get_simple_roundtrip(origin, destination, date, passengers):
    params = construct_query_params([origin, destination], [destination, origin], [date, date + timedelta(days=5)],
                                    passengers)
    r = requests.get(QUERY_BASE + CREATE_SESSION_BASE, params=params, headers=HEADERS)
    j = r.json()
    searchid = j["searchid"]
    time.sleep(30)
    poll = requests.get(QUERY_BASE + POLL_BASE, params={"searchid": searchid, "currency": "USD", "bags": 0}, headers=HEADERS)
    p = poll.json()
    return r.json()


q = get_simple_roundtrip("tel aviv", "rome",  datetime(year=2020, month=3, day=11), 2)

# q = requests.get(QUERY_BASE + CREATE_SESSION_BASE, params={"cabin": "e", "origin1": "TLV", "destination1": "HAN",
#                                                        "nearbyO1": True, "nearbyD1": True,
#                                                        "depart_time1": date_to_query_fromat(datetime(year=2019, month=10, day=11)),
#                                                        "depart_date_flex1": True},
#              headers=HEADERS)
# q = requests.get(QUERY_BASE + CREATE_SESSION_BASE + "bags=0&cabin=e&passengers=5&origin1=TLV&destination1=HAN&departdate1=2019-10-10&currency=USD",
#                  headers=HEADERS)
x = 7