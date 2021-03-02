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


def make_result_geojson():

    # initialize a baseline model object
    swmm_result = swmmio.Model(data_dir + 'scenario.inp')

    if not swmm_result.rpt_is_valid():
        print("report file is not valid")
        return False

    print(swmm_result.rpt.headers)
    for header in swmm_result.rpt.headers:
        print(header)

    #print(type(swmm_result.rpt.subcatchment_results['Subcatchment Sub000']))

    #print(swmm_result.rpt.subcatchment_results.index)
    print(swmm_result.rpt.subcatchment_results.info)
    #print(swmm_result.subcatchments.dataframe.index)
    #for col in swmm_result.subcatchments.dataframe.columns:
     #   print(col)


    print(swmm_result.subcatchments.dataframe.loc['Sub000','TotalRunoffIn'])



if __name__ == "__main__":
    make_result_geojson()

