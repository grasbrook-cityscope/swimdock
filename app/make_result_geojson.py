import os
#import swmmio

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
    #from pyswmm import Simulation, Subcatchments
    #with Simulation('../data/scenario.inp', '../data/test_report.rpt', None) as sim:
        #s1 = Subcatchments(sim)["Sub000"]
        #print(sim.system_units)
        # for step in sim:
        #     #print("time: ", sim.current_time)
        #     #print(s1.runoff)
        # pass
    #sim.report()
    #sim.close()

    print("testing tookit")

    from swmm.toolkit import solver
    solver.swmm_run('../data/scenario.inp', '../data/scenario_test_toolkit.rpt', '../data/scenario_test_toolkit.out')

    from swmm.toolkit import output, shared_enum, output_metadata
    _handle = output.init()
    output.open(_handle, '../data/scenario_test_toolkit.out')

    print("  \n")

    name = output.get_elem_name(_handle, shared_enum.SubcatchResult, 1)
    run_offs = output.get_subcatch_series(_handle, 0, shared_enum.SubcatchAttribute.RUNOFF_RATE, 0, 4*60)
    output.close(_handle)

    print(name)
    print(run_offs)

    exit()



    from pyswmm import Simulation, Subcatchments
    with Simulation(data_dir + 'scenario.inp') as sim:
        sim.start()
        print(sim.report())

        for subcatchment in Subcatchments(sim):
            print(subcatchment.statistics)
            print(subcatchment.runoff)
            print(subcatchment.subcatchmentid)

    exit()
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

    # TODO use



if __name__ == "__main__":
    make_result_geojson()

