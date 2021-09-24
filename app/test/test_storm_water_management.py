import os

from models import ScenarioPaths
from storm_water_management import compute_swmm


class TestScenarioPaths(ScenarioPaths):
    @property
    def input(self):
        return os.path.join(
            os.path.dirname(__file__), "fixtures", "blockToPark_extensive_2.inp"
        )


def test_compute_swmm(tmpdir):
    scenario_paths = TestScenarioPaths(
        id="testId",
        base=tmpdir,
    )
    compute_swmm(scenario_paths)
    assert os.path.isfile(scenario_paths.input)
    assert os.path.isfile(scenario_paths.report)
    assert os.path.isfile(scenario_paths.output)
