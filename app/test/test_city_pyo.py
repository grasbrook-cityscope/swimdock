import pytest
import requests
from city_pyo import CITY_PYO_URL, fetch_user_id


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
