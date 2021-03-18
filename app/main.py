import requests
import json
import os
import time

from make_inp_file import make_inp_file
from make_result_geojson import get_result_geojson

known_hashes = {}

cwd = os.getcwd()
data_dir = (os.path.dirname(cwd) + "/data/").replace("//", "/")
cityPyoUrl = 'https://nc.hcu-hamburg.de/cityPyo/'


# login to cityPyo using the local user_cred_file
# saves the user_id as global variable
def get_city_pyo_user_id(user_cred):
    print("login in to cityPyo")
    response = requests.post(cityPyoUrl + "login", json=user_cred)

    return response.json()['user_id']


# get the stormwater scenarios from cityPyo
def get_stormwater_scenarios():
    data = {
        "userid":user_id,
        "layer":"stormwater_scenario"
        }

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


# creates an input file from user_input and run the simulation
def perform_swmm_analysis(user_input):
    print("making input file")
    make_inp_file(user_input)

    print("computing")
    from swmm.toolkit import solver
    solver.swmm_run('../data/scenario.inp', '../data/scenario.rpt', '../data/scenario.out')


# sends the response to cityPyo, creating a new file as myHash.json
def send_response_to_cityPyo(scenario_hash):
    print("\n sending to cityPyo")
    result = get_result_geojson()

    try:
        query = scenario_hash
        data = {
            "userid": user_id,
            "data": result
        }
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
    with open(cwd + "/" + "cityPyoUser.json", "r") as city_pyo_users:
        users = json.load(city_pyo_users)

    # get user id's to eternally check for new scenario data for each user
    user_ids = []
    for user_cred in users["users"]:
        user_ids.append(get_city_pyo_user_id(user_cred))

    for user_id in user_ids:
        # init known hashes for user
        known_hashes[user_id] = {}

    # loop forever
    while True:
        for user_id in user_ids:
            # compute results for each scenario
            scenarios = get_stormwater_scenarios()
            for scenario_id in scenarios.keys():
                compute = False
                try:
                    old_hash = known_hashes[user_id][scenario_id]
                    if old_hash != scenarios[scenario_id]["hash"]:
                        # new hash, recomputation needed
                        compute = True
                except KeyError:
                    # no result hash known for scenario_id. Compute result.
                    compute = True

                if compute:
                    perform_swmm_analysis(scenarios[scenario_id])
                    send_response_to_cityPyo(scenarios[scenario_id]["hash"])
                    known_hashes[user_id][scenario_id] = scenarios[scenario_id]["hash"]

            time.sleep(1)
