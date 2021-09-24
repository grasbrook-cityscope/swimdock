import json
import os
from models import ScenarioPaths
from make_inp_file import make_inp_file


def test_user_data():
    with open(
        os.path.join(os.path.dirname(__file__), "fixtures", "stormwater_scenario.json"),
        "r",
    ) as stormwater_scenario:
        return json.load(stormwater_scenario)


def test_make_inp_file(tmpdir):
    expected = open(
        os.path.join(os.path.dirname(__file__), "fixtures", "scenario.inp"),
        "r",
    ).read()
    baseline_file = os.path.join(os.path.dirname(__file__), "fixtures", "baseline.inp")
    scenario_pahts = ScenarioPaths(
        id="testId", baseline_input=baseline_file, base=tmpdir
    )
    make_inp_file(test_user_data(), scenario_pahts)
    result = open(
        scenario_pahts.input,
        "r",
    ).read()

    assert result == expected
