import json
import os

from make_inp_file import make_inp_file


def test_user_data():
    with open(
        os.path.join(os.path.dirname(__file__), "fixtures", "stormwater_scenario.json"),
        "r",
    ) as stormwater_scenario:
        return json.load(stormwater_scenario)


def test_make_inp_file():
    expected = open(
        os.path.join(os.path.dirname(__file__), "fixtures", "scenario.inp"),
        "r",
    ).read()
    make_inp_file(test_user_data())
    result = open(
        os.path.join(os.path.dirname(__file__), "fixtures", "scenario.inp"),
        "r",
    ).read()

    assert result == expected
