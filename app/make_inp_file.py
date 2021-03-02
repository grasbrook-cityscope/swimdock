import os
import swmmio

cwd = os.getcwd()
data_dir = os.path.dirname(cwd) + "/data/"

# no longer needed. we are reading rain gages from individual input files instead
# def get_timeseries_df(return_period, duration):
#     name = "%01d-yr_%02d-min" % (return_period, duration)
#
#     all_timeseries_df = pd.read_csv(data_dir + "timeseries.csv", sep=" ")
#     timeseries_df = all_timeseries_df[all_timeseries_df['Name'] == name]
#
#     return timeseries_df


def make_inp_file(user_input):

    # initialize a baseline model object
    baseline = swmmio.Model(data_dir + 'baseline.inp')

    # create a dataframe of the model's subcatchments
    subs = baseline.inp.subcatchments

    print(subs.head())

    for update in user_input["model_updates"]:
        # update the outlet_id in the row of subcatchment_id
        subs.loc[update["subcatchment_id"], ['Outlet']] = update['outlet_id']
        baseline.inp.subcatchments = subs

    print(baseline.inp.subcatchments.head)

    for i, row in subs.iterrows():
        subs.at[i, 'Raingage'] = 'RainGage' + '_' + str(user_input["rain_event"]["return_period"])

    new_file_path = data_dir + 'input.inp'

    # Overwrite the SUBCATCHMENT section of the new model with the adjusted data
    baseline.inp.save(new_file_path)



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

