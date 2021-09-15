from typing import Optional
import requests

CITY_PYO_URL = "https://nc.hcu-hamburg.de/cityPyo/"


def fetch_user_id(user_cred: dict) -> str:
    print("logging in to cityPyo")
    response = requests.post(CITY_PYO_URL + "login", json=user_cred)
    if response.status_code == 401:
        print("user credentials not valid")
        raise Warning("User credentials invalid")
    return response.json()["user_id"]


def fetch_stormwater_scenarios(user_id: str) ->Optional(dict):
    data = {"userid": user_id, "layer": "stormwater_scenario"}

    try:
        response = requests.get(CITY_PYO_URL + "getLayer", json=data)
        response.raise_for_status()
        return response.json()
    # exit on request exception (cityIO down)
    except requests.exceptions.RequestException as e:
        print("could not get from cityPyo")
        print("CityPyo error. " + str(e))
        return None
