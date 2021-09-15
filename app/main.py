from city_pyo import fetch_stormwater_scenarios, fetch_user_id
import os
import time

import requests

import users
from storm_water_management import perform_swmm_analysis
from make_result_geojson import get_result_geojson

cwd = os.getcwd()
data_dir = (os.path.dirname(cwd) + "/data/").replace("//", "/")
cityPyoUrl = "https://nc.hcu-hamburg.de/cityPyo/"


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
    processed_scenarios = {}
    # load cityPyo users from config
    usersDict = users.readUserCredentials()
    # get user id's to eternally check for new scenario data for each user
    user_ids = []
    for user_cred in usersDict["users"]:
        try:
            user_ids.append(fetch_user_id(user_cred))
        except:
            print("Could not authenticate user", user_cred["username"])

    for user_id in user_ids:
        # init known hashes for user
        processed_scenarios[user_id] = {}

    # loop forever
    while True:
        for user_id in user_ids:
            # compute results for each scenario
            scenarios = fetch_stormwater_scenarios(user_id)
            for scenario_id in scenarios.keys():
                try:
                    processed_scenario = processed_scenarios[user_id][scenario_id]
                    if processed_scenario != scenarios[scenario_id]["hash"]:
                        # new hash, recomputation needed
                        scenario = scenarios[scenario_id]
                        perform_swmm_analysis(scenario)
                        send_response_to_cityPyo(scenario["hash"])
                        processed_scenarios[user_id][scenario_id] = scenario["hash"]
                except KeyError:
                    pass  # no result hash known for scenario_id. Compute result.

            time.sleep(1)
