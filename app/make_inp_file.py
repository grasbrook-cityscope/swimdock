import swmmio
from models import CityPyoLayer, CityPyoUser, ScenarioPaths
from typing import Any

def make_inp_file(user_input: CityPyoLayer, scenario_paths: ScenarioPaths):
    # initialize a baseline model object
    baseline = swmmio.Model(scenario_paths.baseline_input)

    # create a dataframe of the model's subcatchments
    subs:Any = baseline.inp.subcatchments

    # reads updates to model from user input and updates the swmmio model
    for update in user_input["model_updates"]:
        # update the outlet_id in the row of subcatchment_id

        subs.loc[update["subcatchment_id"], ["Outlet"]] = update["outlet_id"]
        baseline.inp.subcatchments = subs

    # set the rain gage from user input as raingage for all subcatchments
    scenario_rain_gage_name = (
        "RainGage" + "_" + str(user_input["rain_event"]["return_period"])
    )
    for i, row in subs.iterrows():
        subs.at[i, "Raingage"] = scenario_rain_gage_name

    # Save the new model with the adjusted data
    baseline.inp.save(scenario_paths.input)


# debugging only
if __name__ == "__main__":

    mock_input:CityPyoLayer = {
        "hash": "yxz123",
        "model_updates": [{"subcatchment_id": "Sub000", "outlet_id": "J_out19"}],
        "rain_event": {"return_period": 10, "duration": 120},
        "calculation_method": "normal",
    }
    import os

    cwd = os.getcwd()
    default_data_dir = (os.path.dirname(cwd) + "/data/").replace("//", "/")
    default_baseline = default_data_dir + "baseline.inp"
    scenario_pahts = ScenarioPaths(
        id="yxz123",
        baseline_input=default_data_dir + "baseline.inp",
        base=default_data_dir,
    )

    make_inp_file(mock_input, scenario_pahts)
