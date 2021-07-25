from banking.models import BankingData
from typing import List

import pytest

from banking.api.views import WSUNNAX

test_data = {
    "customer": {
        "name": "Pepito Perez",
        "phone": "+34644323221",
        "email": "pepito@perez.com",
        "address": "Carrer de Girona, 90, 08009 Barcelona",
        "doc": "Y3216434F",
        "participation": "Titular",
    },
    "accounts": [
        {
            "name": "Cuenta personal",
            "number": "ES232100123303030032",
            "currency": "EUR",
            "balance": "352",
            "statements": [
                {
                    "date": "2018-07-05",
                    "amount": "-30",
                    "balance": "352",
                    "concept": "Bar Pepe",
                },
                {
                    "date": "2018-06-15",
                    "amount": "100",
                    "balance": "382",
                    "concept": "Transferencia",
                },
                {
                    "date": "2018-06-02",
                    "amount": "-20",
                    "balance": "282",
                    "concept": "Compra online",
                },
                {
                    "date": "2018-05-11",
                    "amount": "80",
                    "balance": "302",
                    "concept": "Transferencia",
                },
                {
                    "date": "2018-04-01",
                    "amount": "-30",
                    "balance": "222",
                    "concept": "Retiro cajero",
                },
                {
                    "date": "2018-01-03",
                    "amount": "-30",
                    "balance": "252",
                    "concept": "Bar Pepe",
                },
            ],
        },
        {
            "name": "Cuenta ahorro",
            "number": "ES232100523522355235",
            "currency": "EUR",
            "balance": "1322.2",
            "statements": [
                {
                    "date": "2018-07-25",
                    "amount": "-12",
                    "balance": "1322.2",
                    "concept": "McDonalds",
                },
                {
                    "date": "2018-07-21",
                    "amount": "280",
                    "balance": "1334.2",
                    "concept": "Nomina",
                },
                {
                    "date": "2018-02-12",
                    "amount": "280",
                    "balance": "1054.2",
                    "concept": "Nomina",
                },
                {
                    "date": "2018-01-01",
                    "amount": "-20",
                    "balance": "774.2",
                    "concept": "Compra online",
                },
                {
                    "date": "2017-07-11",
                    "amount": "-20",
                    "balance": "794.2",
                    "concept": "Compra online",
                },
            ],
        },
    ],
}


@pytest.fixture
def banking_data() -> BankingData:
    BankingData.objects.create(code="fixture")
    ws = WSUNNAX("username", "password")
    ws.data = test_data
    ws.save_data("fixture")
    bkd = BankingData.objects.get(code="fixture")
    return bkd


@pytest.fixture
def banking_delete_data() -> BankingData:
    BankingData.objects.create(code="fixture_delete")
    ws = WSUNNAX("username", "password")
    ws.data = test_data
    print(ws.data)
    ws.save_data("fixture_delete")
    bkd = BankingData.objects.get(code="fixture_delete")
    return bkd


# @pytest.fixture
# def companies(request, company) -> List[Company]:
#     companies = []
#     names = request.param
#     for name in names:
#         companies.append(company(name=name))
#     return companies


# @pytest.fixture()
# def company(**kwargs):
#     def _company_factory(**kwargs) -> Company:
#         company_name = kwargs.pop("name", "Test Company INC")
#         return Company.objects.create(name=company_name, **kwargs)

#     return _company_factory
