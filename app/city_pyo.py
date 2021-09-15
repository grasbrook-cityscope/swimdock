import requests

CITY_PYO_URL = "https://nc.hcu-hamburg.de/cityPyo/"


def fetch_user_id(user_cred: dict) -> str:
    print("loging in to cityPyo")
    response = requests.post(CITY_PYO_URL + "login", json=user_cred)
    if response.status_code == 401:
        print("user credentials not valid")
        raise Warning("User credentials invalid")
    return response.json()["user_id"]


def fetch_stormwater_scenarios(user_id: str):
    data = {"userid": user_id, "layer": "stormwater_scenario"}

    try:
        response = requests.get(CITY_PYO_URL + "getLayer", json=data)

        if not response.status_code == 200:
            print("could not get from cityPyo")
            print("Error code", response.status_code)
            # todo raise error and return error
            return {}
    # exit on request execption (cityIO down)
    except requests.exceptions.RequestException as e:
        print("CityPyo error. " + str(e))

        return None

    return response.json()
