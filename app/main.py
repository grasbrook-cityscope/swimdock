import time

import users
from city_pyo import fetch_stormwater_scenarios, fetch_user_id, send_geojson
from storm_water_management import perform_swmm_analysis

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
                        geo_json = perform_swmm_analysis(scenario)
                        send_geojson(user_id, scenario["hash"], geo_json)
                        processed_scenarios[user_id][scenario_id] = scenario["hash"]
                except KeyError:
                    pass  # no result hash known for scenario_id. Compute result.

            time.sleep(1)
