from make_inp_file import make_inp_file
from make_result_geojson import get_result_geojson


# creates an input file from user_input, runs the simulation and returns the output in geojson
def perform_swmm_analysis(user_input) -> dict:
    print("making input file")
    make_inp_file(user_input)
    compute_swmm()
    return get_result_geojson()


def compute_swmm(scenario_location="../data/scenario.inp"):
    print("computing")
    from swmm.toolkit import solver

    solver.swmm_run(scenario_location, "../data/scenario.rpt", "../data/scenario.out")
