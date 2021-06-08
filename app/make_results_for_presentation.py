import requests
import json
import os
import time

from make_result_geojson import get_result_geojson

known_hashes = {}

cwd = os.getcwd()
data_dir = (os.path.dirname(cwd) + "/data/").replace("//", "/")
input_files_dir = (os.path.dirname(cwd) + "/data/input_files").replace("//", "/")


def perform_swmm_analysis(input_file_name):
    print("computing")
    from swmm.toolkit import solver
    solver.swmm_run('../data/scenario.inp', '../data/scenario.rpt', '../data/scenario.out')



if __name__ == "__main__":


    input_file_name = "blockToPark_extensive_2.inp"
    perform_swmm_analysis(input_file_name)
    result_geojson = get_result_geojson()

    print(result_geojson)


    # todo write result geojson to disk

