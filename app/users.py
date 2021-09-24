import json
import os
from typing import Final
from models import CityPyoUsers
cwd: Final = os.getcwd()


def readUserCredentialsFromFile(file: str) -> CityPyoUsers:
    with open(file, "r") as city_pyo_users:
        return json.load(city_pyo_users)


def readUserCredentials() -> CityPyoUsers:
    return readUserCredentialsFromFile(cwd + "/cityPyoUser.json")
