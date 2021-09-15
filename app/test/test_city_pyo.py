import json
import os
import pytest
import requests
from city_pyo import CITY_PYO_URL, fetch_stormwater_scenarios, fetch_user_id


def test_success(requests_mock):
    requests_mock.post(
        CITY_PYO_URL + "login",
        json={"restricted": False, "user_id": "35866b18-b5c5-4b95-9b37-fa8d69dac4c0"},
    )
    assert "35866b18-b5c5-4b95-9b37-fa8d69dac4c0" == fetch_user_id({"username": "name"})


def test_user_not_allowed(requests_mock):
    requests_mock.post(CITY_PYO_URL + "login", status_code=401)
    with pytest.raises(Warning, match=r".*credentials invalid.*"):
        fetch_user_id({"username": "name"})


def test_remote_exception(requests_mock):
    requests_mock.post(CITY_PYO_URL + "login", exc=requests.exceptions.ConnectTimeout)
    with pytest.raises(requests.exceptions.ConnectTimeout):
        fetch_user_id({"username": "name"})


def test_fetch_stormwater_scenarios_remote_error(requests_mock):
    requests_mock.get(CITY_PYO_URL + "getLayer", status_code=400)
    assert fetch_stormwater_scenarios("userId") == None

def test_fetch_stormwater_scenarios_connection_error(requests_mock):
    requests_mock.get(CITY_PYO_URL + "getLayer", exc=requests.exceptions.ConnectTimeout)
    assert fetch_stormwater_scenarios("userId") == None

def stormwater_scenario():
    with open(
        os.path.join(os.path.dirname(__file__), "fixtures", "stormwater_scenario.json"),
        "r",
    ) as stormwater_scenario:
        return json.load(stormwater_scenario)

def test_fetch_stormwater_scenarios(requests_mock):
    requests_mock.get(CITY_PYO_URL + "getLayer", json=[stormwater_scenario()])
    assert fetch_stormwater_scenarios("userId") == [stormwater_scenario()]
