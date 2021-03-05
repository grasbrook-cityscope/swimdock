import requests
import json
import os
import time

from make_inp_file import make_inp_file
from make_result_geojson import get_result_geojson

known_hashes = {}
user_id = None

cwd = os.getcwd()
data_dir = os.path.dirname(cwd) + "/data/"
cityPyoUrl = 'https://nc.hcu-hamburg.de/cityPyo/'

# login to cityPyo using the local user_cred_file
# saves the user_id as global variable
def cityPyo_login():
    print("login in to cityPyo")
    with open(cwd + "/" + "cityPyoUser.json", "r") as user_cred_file:
        user_cred = json.load(user_cred_file)

    response = requests.post(cityPyoUrl + "login", json=user_cred)

    global user_id
    user_id = response.json()['user_id']


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
            # todo : we need an error tracker!
        else:
            print("\n")
            print("result send to cityPyo.", "Result hash is: ", scenario_hash)
            print("waiting for new input...")
        # exit on request exception (cityIO down)
    except requests.exceptions.RequestException as e:
        print("CityPyo error. " + str(e))


# Compute loop to run eternally
if __name__ == "__main__":
    cityPyo_login()

    # loop forever
    while True:
        scenarios = get_stormwater_scenarios()

        # compute results for each scenario
        for scenario_id in scenarios.keys():
            compute = False
            try:
                old_hash = known_hashes[scenario_id]
                if old_hash != scenarios[scenario_id]["hash"]:
                    # new hash, recomputation needed
                    compute = True
            except KeyError:
                # no result hash known for scenario_id. Compute result.
                compute = True

            if compute:
                perform_swmm_analysis(scenarios[scenario_id])
                send_response_to_cityPyo(scenarios[scenario_id]["hash"])
                known_hashes[scenario_id] = scenarios[scenario_id]["hash"]

        time.sleep(1)
