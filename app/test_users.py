import users


def test_readUserCredentialsFromFile():
    assert users.readUserCredentialsFromFile("_test_fixtures/fixturePyoUser.json") == {'users': [{'password': 'blubb', 'username': 'testuser'}]}
