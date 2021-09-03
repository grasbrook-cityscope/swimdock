import os
import time

import requests

import users
from storm_water_management import perform_swmm_analysis
from make_result_geojson import get_result_geojson

known_hashes = {}

cwd = os.getcwd()
data_dir = (os.path.dirname(cwd) + "/data/").replace("//", "/")
cityPyoUrl = "https://nc.hcu-hamburg.de/cityPyo/"


# login to cityPyo using the local user_cred_file
# saves the user_id as global variable
def get_city_pyo_user_id(user_cred):
    print("login in to cityPyo")
    response = requests.post(cityPyoUrl + "login", json=user_cred)
    if response.status_code == 401:
        print("user credentials not valid")
        raise Warning("User credentials invalid")
    return response.json()["user_id"]


# get the stormwater scenarios from cityPyo
def get_stormwater_scenarios():
    data = {"userid": user_id, "layer": "stormwater_scenario"}

    try:
        response = requests.get(cityPyoUrl + "getLayer", json=data)

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


# sends the response to cityPyo, creating a new file as myHash.json
def send_response_to_cityPyo(scenario_hash):
    print("\n sending to cityPyo")
    result = get_result_geojson()

    try:
        query = scenario_hash
        data = {"userid": user_id, "data": result}
        response = requests.post(cityPyoUrl + "addLayerData/" + query, json=data)

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


# Compute loop to run eternally
if __name__ == "__main__":
    # load cityPyo users from config
    usersDict = users.readUserCredentials()
    # get user id's to eternally check for new scenario data for each user
    user_ids = []
    for user_cred in usersDict["users"]:
        try:
            user_ids.append(get_city_pyo_user_id(user_cred))
        except:
            print("Could not authenticate user", user_cred["username"])

    for user_id in user_ids:
        # init known hashes for user
        known_hashes[user_id] = {}

    # loop forever
    while True:
        for user_id in user_ids:
            # compute results for each scenario
            scenarios = get_stormwater_scenarios()
            for scenario_id in scenarios.keys():
                try:
                    old_hash = known_hashes[user_id][scenario_id]
                    if old_hash != scenarios[scenario_id]["hash"]:
                        # new hash, recomputation needed
                        scenario = scenarios[scenario_id]
                        perform_swmm_analysis(scenario)
                        send_response_to_cityPyo(scenario["hash"])
                        known_hashes[user_id][scenario_id] = scenario["hash"]
                except KeyError:
                    pass  # no result hash known for scenario_id. Compute result.

            time.sleep(1)
