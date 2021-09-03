import os
import swmmio

cwd = os.getcwd()
default_data_dir = (os.path.dirname(cwd) + "/data/").replace("//", "/")
default_baseline = default_data_dir + 'baseline.inp'
default_scenario = default_data_dir + 'scenario.inp'

def make_inp_file(user_input, baseline_file=default_baseline, scenario_output=default_scenario):
    # initialize a baseline model object
    baseline = swmmio.Model(baseline_file)

    # create a dataframe of the model's subcatchments
    subs = baseline.inp.subcatchments

    # reads updates to model from user input and updates the swmmio model
    for update in user_input["model_updates"]:
        # update the outlet_id in the row of subcatchment_id

        subs.loc[update["subcatchment_id"], ['Outlet']] = update['outlet_id']
        baseline.inp.subcatchments = subs

    # set the rain gage from user input as raingage for all subcatchments
    scenario_rain_gage_name = 'RainGage' + '_' + str(user_input["rain_event"]["return_period"])
    for i, row in subs.iterrows():
        subs.at[i, 'Raingage'] = scenario_rain_gage_name

    # Save the new model with the adjusted data
    baseline.inp.save(scenario_output)


# debugging only
if __name__ == "__main__":

    mock_input = {
        "hash": "yxz123",
        "model_updates":
        [
          {
              "subcatchment_id": "Sub000",
              "outlet_id": "J_out19"
          }
        ],
        "rain_event" : {
          "return_period": 10,
          "duration": 120
        },
        "calculation_method": "normal"
      }

    make_inp_file(mock_input)

