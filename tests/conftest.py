import pytest
from app import main


@pytest.fixture
def client():
    main.app.config["TESTING"] == True
    with main.app.test_client() as client:
        yield client
