import os
from typing import Final

from storm_water_management import compute_swmm

cwd: Final = os.getcwd()


def test_compute_swmm():
    compute_swmm(cwd + "/test/fixtures/blockToPark_extensive_2.inp")
    assert os.path.isfile("../data/scenario.rpt")
    assert os.path.isfile("../data/scenario.out")
