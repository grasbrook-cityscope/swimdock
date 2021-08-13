from make_inp_file import make_inp_file


# creates an input file from user_input and run the simulation
def perform_swmm_analysis(user_input):
    print("making input file")
    make_inp_file(user_input)
    compute_swmm()


def compute_swmm(scenario_location="../data/scenario.inp"):
    print("computing")
    from swmm.toolkit import solver

    solver.swmm_run(scenario_location, "../data/scenario.rpt", "../data/scenario.out")
