import json, time
from typing import List

import pytest
from django.urls import reverse

from banking.models import BankingData, Customer, Account, Statement

read_url = reverse("read", kwargs={"code": "example1"})
code = "123456"
data = {"username": "Y3216434F", "password": "pperez2018"}
pytestmark = pytest.mark.django_db


def test_create_read_without_arguments_should_fail(client) -> None:
    response = client.post(path=read_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "message": "Username and password are required."
    }


def test_create_read_existing_code_should_fail(client) -> None:
    BankingData.objects.create(code=code)
    read_url = reverse("read", kwargs={"code": code})
    response = client.post(
        path=read_url, data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "message": "Bad request, the search code must be unique"
    }


def test_create_read_code_twice_should_fail(client) -> None:
    read_url = reverse("read", kwargs={"code": code})
    response = client.post(
        path=read_url, data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert json.loads(response.content) == {"status": "PENDING"}
    response = client.post(
        path=read_url, data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "message": "Bad request, the search code must be unique"
    }


def test_get_code_exists_should_succeed(client, banking_data) -> None:
    read_url = reverse("read", kwargs={"code": banking_data.code})
    response = client.get(path=read_url)
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("status") == "DONE"
    assert "customer" in response_content.get("data")
    customer = Customer.objects.get(banking_data__code=banking_data.code)
    assert response_content.get("data").get("customer").get("name") == customer.name
    assert (
        response_content.get("data").get("customer").get("participation")
        == customer.participation
    )
    assert response_content.get("data").get("customer").get("email") == customer.email
    assert response_content.get("data").get("customer").get("phone") == customer.phone
    accounts = Account.objects.filter(customer=customer)
    assert accounts.count() == len(response_content.get("data").get("accounts"))
    statements = Statement.objects.filter(account__customer=customer).count()
    response_statements_list = []
    for ac in response_content.get("data").get("accounts"):
        for s in ac.get("statements"):
            response_statements_list.append(s)
    assert statements == len(response_statements_list)


def test_get_code_not_exists_should_fail(client) -> None:
    read_url = reverse("read", kwargs={"code": "arandomcode"})
    response = client.get(path=read_url)
    response_content = json.loads(response.content)
    assert response.status_code == 404
    assert response_content == {"detail": "Not found."}


# def test_delete_code_exists_should_succeed(client, banking_delete_data) -> None:
#     # customer = Customer.objects.get(banking_data__code=banking_data.code)
#     print("AQUIIII!!!!!!!!!")
#     print(banking_delete_data.code)
#     read_url = reverse("read", kwargs={"code": banking_delete_data.code})
#     response = client.delete(path=read_url)
#     assert 204 == 204