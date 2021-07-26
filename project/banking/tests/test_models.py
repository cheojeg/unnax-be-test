import json
import pytest
from banking.models import BankingData, Customer, Account, Statement

pytestmark = pytest.mark.django_db

customer_data = {
    "name": "Jose Garcia",
    "phone": "+18498899154",
    "email": "cheojeg@unnax.com",
    "address": "Carrer de Girona, 90, 08009 Barcelona",
    "doc": "v191944334",
    "participation": "Titular",
}

account_data = {
    "name": "Cuenta personal",
    "number": "ES232100123303030032",
    "currency": "EUR",
    "balance": "352",
}

staments_data = [
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
]


def test_banking_data_model() -> None:
    bkd = BankingData.objects.create(code="code_test")
    assert bkd.__str__() == "code_test"
    bkd_count = BankingData.objects.filter(code="code_test").count()
    assert bkd_count == 1


def test_customer_model() -> None:
    bkd = BankingData.objects.create(code="code_test")
    customer_count = Customer.objects.filter(banking_data__code=bkd.code).count()
    assert customer_count == 0
    customer = Customer.objects.create(banking_data=bkd, **customer_data)
    assert customer.name == customer_data["name"]
    assert customer.address == customer_data["address"]
    assert customer.phone == customer_data["phone"]
    assert customer.email == customer_data["email"]
    assert customer.doc == customer_data["doc"]
    assert customer.participation == customer_data["participation"]
    name = customer_data["name"]
    assert customer.__str__() == f"code_test - {name}"
    customer_count = Customer.objects.filter(banking_data__code=bkd.code).count()
    assert customer_count == 1


def test_account() -> None:
    bkd = BankingData.objects.create(code="code_test")
    customer = Customer.objects.create(banking_data=bkd, **customer_data)
    account = account_data
    account = Account.objects.create(customer=customer, **account)
    assert account.name == account_data["name"]
    assert account.number == account_data["number"]
    assert account.currency == account_data["currency"]
    assert account.balance == account_data["balance"]
    assert account.customer == customer
    assert account.__str__() == f"{bkd.code} - {account.number}"
    customer_count = Account.objects.filter(customer=customer).count()
    assert customer_count == 1


def test_statement() -> None:
    bkd = BankingData.objects.create(code="code_test")
    customer = Customer.objects.create(banking_data=bkd, **customer_data)
    account = account_data
    account = Account.objects.create(customer=customer, **account)
    for s in staments_data:
        Statement.objects.create(account=account, **s)
    st_query = statements_count = Statement.objects.filter(account=account)
    st_first = st_query.first()
    assert st_first.concept == "Bar Pepe"
    assert st_first.amount == -30
    assert st_first.balance == 352
    assert st_first.date.strftime("%Y-%m-%d") == "2018-07-05"
    assert st_first.__str__() == f"{st_first.account.number} - {st_first.id}"
    statements_count = st_query.count()
    assert statements_count == len(staments_data)