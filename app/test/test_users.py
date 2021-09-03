import os
import users
from typing import Final

cwd: Final = os.getcwd()

def test_readUserCredentialsFromFile():
    assert users.readUserCredentialsFromFile(cwd+"/test/fixtures/fixturePyoUser.json") == {
        "users": [{"password": "blubb", "username": "testuser"}]
    }
