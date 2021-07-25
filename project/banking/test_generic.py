import requests
import json
import time

testing_read_url = "http://localhost:8000/read/example1"
data = {"username": "Y3216434F", "password": "pperez2018"}


def test_read_agnostic() -> None:
    response = requests.post(
        url=testing_read_url,
        json=data,
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "PENDING"
    time.sleep(6)
    response = requests.get(url=testing_read_url)
    assert response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content.get("status") == "DONE"
    assert "data" in response_content
    assert "customer" in response_content.get("data")
    assert "doc" in response_content.get("data").get("customer")
    assert data["username"] in response_content.get("data").get("customer").get("doc")
    cleanup_read()


def cleanup_read() -> None:
    response = requests.delete(url=testing_read_url)
    assert response.status_code == 204