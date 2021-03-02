import requests
import json
import os
import subprocess
import time
from make_inp_file import make_inp_file


known_hashes = {}
user_id = None

cwd = os.getcwd()
data_dir = os.path.dirname(cwd) + "/data/"
cityPyoUrl = 'http://localhost:5000/'



def cityPyoLogin():
    with open(cwd + "/" + "cityPyoUser.json", "r") as user_cred_file:

        user_cred = json.load(user_cred_file)

    response = requests.post(cityPyoUrl + "login", json=user_cred)

    global user_id
    user_id = response.json()['user_id']





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


def perform_swmm_analysis(user_input):
    make_inp_file(user_input)

    # run swim
    args = ('./swmm51015_engine/build/runswmm5', '../data/input.inp', '../data/out.rpt')
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    out, err = popen.communicate()
    print(out)
    if err:
        print("there was an error in the swmm process")
        print(err)
    else:
        print("i swam!!")


    exit()


    # TODO get geojson to read specific information for subcatchments  // ideally the whole input file would be parsed from that geojson.
    # how as long as most infromation is static for now , we use a static baseline.inp for now.


    # todo : if user_input -> calculation method == "extensive"
    # create a computation loop
    # user_input.copy() , custom user_input["rain_event"] for each rain in extensive calc


    # TODO
    #calculate()
    #make_output_json()


if __name__ == "__main__":

    cityPyoLogin()

    # loop forever
    while True:
        scenarios = get_stormwater_scenarios()

        for scenario_id in scenarios.keys():
            try:
                old_hash = known_hashes[scenario_id]
                if old_hash is not scenarios[scenario_id]["hash"]:
                    # new hash
                    perform_swmm_analysis(scenarios[scenario_id])
            except KeyError:
                # no hash known for scenario_id
                perform_swmm_analysis(scenarios[scenario_id])

        time.sleep(2)




# import os
# import swmmio
# import pandas as pd
#
# from pathlib import Path
# cwd = os.getcwd()
# data_dir = os.path.dirname(cwd) + "/data/"
#
# # initialize a baseline model object
# baseline = swmmio.Model(data_dir + 'baseline.inp')
#
# rpt = baseline.rpt
#
# print(baseline.timeseries)
#
#
# from swmmio.core import rpt
# from swmmio.tests.data import RPT_FULL_FEATURES
#
# report = rpt(RPT_FULL_FEATURES)
#
# print("summeary")
# print(report.cross_section_summary)
#
# from swmmio.examples import spruce
#
# print(spruce.rpt.link_results)
#
#
# exit()
#
#
# # create a dataframe of the model's subcatchments
# subs = baseline.inp.subcatchments
#
# # TODO get subcatchments to be updated from scenario.json
# updates = [
#     {
#         "subcatchment_id": "S5",
#         "outlet_id": "the_user_changed_this",
#     }
# ]
#
# print(subs.head())
#
# for update in updates:
#     # update the outlet_id in the row of subcatchment_id
#     subs.loc[update["subcatchment_id"], ['Outlet']] = update['outlet_id']
#     baseline.inp.subcatchments = subs
#
# print(baseline.inp.subcatchments.head)
#
# # copy the base model into a new directory
# newfilepath = data_dir + 'input.inp'
#
# # Overwrite the SUBCATCHMENT section of the new model with the adjusted data
# baseline.inp.save(newfilepath)