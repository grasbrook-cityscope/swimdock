from make_inp_file import make_inp_file
from make_result_geojson import get_result_geojson
from models import CityPyoLayer, ScenarioPaths

# creates an input file from user_input, runs the simulation and returns the output in geojson
def perform_swmm_analysis(user_input:CityPyoLayer, scenario_paths:ScenarioPaths) -> dict:
    print("making input file")
    make_inp_file(user_input, scenario_paths)
    compute_swmm(scenario_paths)
    return get_result_geojson()


def compute_swmm(scenario_paths:ScenarioPaths):
    print("computing")
    from swmm.toolkit import solver

    solver.swmm_run(scenario_paths.input, scenario_paths.report, scenario_paths.output)
