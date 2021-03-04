import os
import json
import swmmio
from swmm.toolkit import output, shared_enum, output_metadata
import datetime

cwd = os.getcwd()
data_dir = os.path.dirname(cwd) + "/data/"
empty_result_geojson = data_dir + 'subcatchments.json'
runoff_enum = shared_enum.SubcatchAttribute.RUNOFF_RATE


# reads simulation duration and report_step_duration from inp file
def get_sim_duration_and_report_step():
    # initialize a model model object
    model = swmmio.Model(data_dir + 'scenario.inp')

    inp_start_date = model.inp.options.loc["START_DATE"].values[0]
    inp_start_time = model.inp.options.loc["START_TIME"].values[0]

    inp_end_date = model.inp.options.loc["END_DATE"].values[0]
    inp_end_time = model.inp.options.loc["END_TIME"].values[0]

    start_time = datetime.datetime.strptime(inp_start_date + ' ' + inp_start_time, '%d/%m/%Y %H:%M:%S')
    end_time = datetime.datetime.strptime(inp_end_date + ' ' + inp_end_time, '%d/%m/%Y %H:%M:%S')
    report_step = datetime.datetime.strptime(model.inp.options.loc["REPORT_STEP"].values[0], '%H:%M:%S').minute

    simulation_duration = int((end_time - start_time).total_seconds() / 60)

    return simulation_duration, report_step


# gets local file subcatchments.geojson
def get_geojson():
    with open(empty_result_geojson, 'r') as file:
        return json.load(file)


# reads the simulation result, returns it in geojson format
def get_result_geojson():
    sim_duration, report_step = get_sim_duration_and_report_step()

    _handle = output.init()
    output.open(_handle, '../data/scenario.out')

    subcatchment_count = output.get_proj_size(_handle)[0]

    # lookup table for result index by subcatchment name
    result_sub_indexes = {}
    for i in range(0, subcatchment_count):
        result_sub_indexes[output.get_elem_name(_handle, shared_enum.SubcatchResult, i)] = i

    # iterate over subcatchemnt features in geojson and get timeseries results for subcatchment
    geojson = get_geojson()
    for feature in geojson["features"]:
        sub_id = result_sub_indexes[feature["properties"]["Name"]]
        run_offs = output.get_subcatch_series(_handle, sub_id, runoff_enum, 0, sim_duration)
        timestamps = [i * report_step for i, val in enumerate(run_offs)]
        feature["properties"]["runoff_results"] = {
            "timestamps": timestamps,
            "runoff_value": run_offs
        }

    output.close(_handle)

    return geojson


if __name__ == "__main__":
    get_result_geojson()

