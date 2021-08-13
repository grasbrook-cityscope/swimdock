import os
import swmmio

cwd = os.getcwd()
default_data_dir = (os.path.dirname(cwd) + "/data/").replace("//", "/")


def make_inp_file(user_input, data_dir=default_data_dir):
    # initialize a baseline model object
    baseline = swmmio.Model(data_dir + 'baseline.inp')

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
    new_file_path = data_dir + 'scenario.inp'
    baseline.inp.save(new_file_path)


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

