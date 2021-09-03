import requests

CITY_PYO_URL = "https://nc.hcu-hamburg.de/cityPyo/"


def fetch_user_id(user_cred:dict) -> str:
    print("loging in to cityPyo")
    response = requests.post(CITY_PYO_URL + "login", json=user_cred)
    if response.status_code == 401:
        print("user credentials not valid")
        raise Warning("User credentials invalid")
    return response.json()["user_id"]
