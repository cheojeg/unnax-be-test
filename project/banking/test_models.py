import json
import pytest
from .models import BankingData, Customer, Account

pytestmark = pytest.mark.django_db

model_data = {
    "customer": {
        "name": "Jose Garcia",
        "phone": "+18498899154",
        "email": "cheojeg@unnax.com",
        "address": "Carrer de Girona, 90, 08009 Barcelona",
        "doc": "v191944334",
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


def test_banking_data_model() -> None:
    bkd = BankingData.objects.create(code="code_test")
    assert bkd.__str__() == "code_test"


def test_customer_model() -> None:
    bkd = BankingData.objects.create(code="code_test")
    customer_count = Customer.objects.filter(banking_data__code=bkd.code).count()
    assert customer_count == 0
    customer = Customer.objects.create(banking_data=bkd, **model_data["customer"])
    assert customer.name == model_data["customer"]['name']
    assert customer.address == model_data["customer"]['address']
    assert customer.phone == model_data["customer"]['phone']
    assert customer.email == model_data["customer"]['email']
    assert customer.doc == model_data["customer"]['doc']
    assert customer.participation == model_data["customer"]['participation']
    customer_count = Customer.objects.filter(banking_data__code=bkd.code).count()
    assert customer_count == 1
