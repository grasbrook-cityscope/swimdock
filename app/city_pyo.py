from typing import Optional

import requests

from make_result_geojson import get_result_geojson

CITY_PYO_URL = "https://nc.hcu-hamburg.de/cityPyo/"


def fetch_user_id(user_cred: dict) -> str:
    print("logging in to cityPyo")
    response = requests.post(CITY_PYO_URL + "login", json=user_cred)
    if response.status_code == 401:
        print("user credentials not valid")
        raise Warning("User credentials invalid")
    return response.json()["user_id"]


def fetch_stormwater_scenarios(user_id: str) -> Optional[dict]:
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


# sends the response to cityPyo, creating a new file as myHash.json
def send_geojson(user_id: str, scenario_hash: str) -> None:
    print("\n sending to cityPyo")
    result = get_result_geojson()

    try:
        query = scenario_hash
        data = {"userid": user_id, "data": result}
        response = requests.post(CITY_PYO_URL + "addLayerData/" + query, json=data)

        if not response.status_code == 200:
            print("could not post to cityPyo")
            print("Error code", response.status_code)
        else:
            print("\n")
            print("result send to cityPyo.", "Result hash is: ", scenario_hash)
            print("waiting for new input...")
        # exit on request exception (cityIO down)
    except requests.exceptions.RequestException as e:
        print("CityPyo error. " + str(e))
