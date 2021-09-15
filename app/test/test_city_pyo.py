import json
import os
import pytest
import requests
from city_pyo import (
    CITY_PYO_URL,
    fetch_stormwater_scenarios,
    fetch_user_id,
    send_geojson,
)


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
    mock_scenarios = {"scenarioId": stormwater_scenario()}
    requests_mock.get(CITY_PYO_URL + "getLayer", json=mock_scenarios)
    assert fetch_stormwater_scenarios("userId") == mock_scenarios


def test_send_geojson_remote_error(requests_mock, capsys):
    scenario_hash = "scenarioHash"
    requests_mock.post(CITY_PYO_URL + "addLayerData/" + scenario_hash, status_code=400)
    send_geojson(user_id="userId", scenario_hash=scenario_hash) == None
    capture_print = capsys.readouterr()
    assert "could not post to cityPyo" in capture_print.out
    assert "Error code 400" in capture_print.out


def test_fetch_stormwater_scenarios_connection_error(requests_mock, capsys):
    scenario_hash = "scenarioHash"
    requests_mock.post(
        CITY_PYO_URL + "addLayerData/" + scenario_hash,
        exc=requests.exceptions.ConnectTimeout,
    )
    send_geojson(user_id="userId", scenario_hash=scenario_hash) 
    capture_print = capsys.readouterr()
    assert "CityPyo error" in capture_print.out

def test_fetch_stormwater_scenarios(requests_mock, capsys):
    scenario_hash = "scenarioHash"
    requests_mock.post(
        CITY_PYO_URL + "addLayerData/" + scenario_hash
    )
    send_geojson(user_id="userId", scenario_hash=scenario_hash) 
    capture_print = capsys.readouterr()
    assert "result send to cityPyo." in capture_print.out
