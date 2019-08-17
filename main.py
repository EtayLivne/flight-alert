import requests
from datetime import datetime
import logging


QUERY_BASE = "https://apidojo-kayak-v1.p.rapidapi.com/flights/"
CREATE_SESSION_BASE = "create-session?"
CABIN_COMPONENT = "cabin=e"
CURRENCY_COMPONENT = "currency=USD"
BAGS_COMPONENT = "bags=0"
PASSENGERS_COMPONENT =  "adults={}"
ORIGIN_COMPONENT = "origin{}={}"
DESTINATION_COMPONENT = "destination{}={}"
DATE_COMPONENT = "departdate{}={}"
HEADERS  = {"X-RapidAPI-Host": "apidojo-kayak-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "a07bbf8525msh0f978afda6b7faep16106djsn80681f0b3680"}

CODE_MAP = {"tel aviv": "TLV",
            "hanoi": "HAN"}

log = logging.getLogger("main")

def city_to_port_code(city):
    if city not in CODE_MAP:
        raise KeyError("unknown airport code for the city {}".format(city))
    return CODE_MAP[city]


def date_to_query_fromat(date):
    return date.strftime("%Y-%m-%d")

def direction_to_query_format(num, origin, destination, date):
    origin = ORIGIN_COMPONENT.format(num, origin)
    destination = DESTINATION_COMPONENT.format(num, destination)
    date = DATE_COMPONENT.format(num, date)
    return "&".join([origin, destination, date])


def construct_query(origin, destination, outbound_date, inbound_date, passengers):
    # format string inputs to query requirements

    origin = city_to_port_code(origin)
    destination = city_to_port_code(destination)
    outbound_date = date_to_query_fromat(outbound_date)
    inbound_date = date_to_query_fromat(inbound_date)

    # construct individual query components
    outbound = direction_to_query_format(1, origin, destination, outbound_date)
    inbound = direction_to_query_format(2, destination, origin, inbound_date)
    cabin = CABIN_COMPONENT
    currency = CURRENCY_COMPONENT
    passengers = PASSENGERS_COMPONENT.format(passengers)
    bags = BAGS_COMPONENT

    # combine into query string
    query_string = "&".join([outbound, inbound, cabin, currency, passengers, bags])
    return QUERY_BASE + CREATE_SESSION_BASE + query_string



q = construct_query("tel aviv", "hanoi", datetime(year=2019, month=9,day=25), datetime(year=2019,month=10,day=11), 5)

r = requests.get(q, headers=HEADERS)

response_content = r.json()

f =4