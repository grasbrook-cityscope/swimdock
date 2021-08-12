import json
import os
from typing import Final

cwd: Final = os.getcwd()


def readUserCredentialsFromFile(file: str):
    with open(cwd + "/" + file, "r") as city_pyo_users:
        return json.load(city_pyo_users)


def readUserCredentials():
    return readUserCredentialsFromFile("cityPyoUser.json")
