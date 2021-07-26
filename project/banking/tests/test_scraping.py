import json, responses, requests
import pytest
from banking.models import BankingData, Customer, Account, Statement
from banking.scripts import Scraping

pytestmark = pytest.mark.django_db

login_html = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
    <title>Accounts</title>

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/js/materialize.min.js"></script>
    <style>
        nav .nav-wrapper {
            background-color: #26a69a;
        }
    </style>
</head>
<body>
    <div class="row">
        <nav>
            <div class="nav-wrapper">
            <a href="account" class="brand-logo">Home</a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
                <li><a href="customer">Settings</a></li>
                <li><a href="logout">Logout</a></li>
            </ul>
            </div>
        </nav>
        <div class="col s6 offset-s3">
            <h4>Accounts</h4>
            <ul class="collection">
                
                <li class="collection-item avatar">
                    <span class="title">Cuenta personal</span>
                    <p>ES232100123303030032 <br>
                    <span >€352</span>
                    </p>
                    <a href="statements/1" class="secondary-content"><i class="material-icons">info_outline</i></a>
                </li>
                
                <li class="collection-item avatar">
                    <span class="title">Cuenta ahorro</span>
                    <p>ES232100523522355235 <br>
                    <span >€1322.2</span>
                    </p>
                    <a href="statements/2" class="secondary-content"><i class="material-icons">info_outline</i></a>
                </li>
                
            </ul>
        </div>
    </div>
</body>
</html>"""

customer_html = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
    <title>Settings</title>

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/js/materialize.min.js"></script>
    <style>
        nav .nav-wrapper {
            background-color: #26a69a;
        }
    </style>
</head>
<body>
    <div class="row">
        <nav>
            <div class="nav-wrapper">
            <a href="account" class="brand-logo">Home</a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
                <li><a href="customer">Settings</a></li>
                <li><a href="logout">Logout</a></li>
            </ul>
            </div>
        </nav>
        <div class="col s6 offset-s3">
            <ul class="collection with-header">
                <li class="collection-header"><h4>Jose Garcia</h4></li>
                <li class="collection-item">+18498123123</li>
                <li class="collection-item">jgarcia@mail.com</li>
                <li class="collection-item">Santo Domingo, Av 27 de Febrero #45</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

account_html = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
    <title>Accounts</title>

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/js/materialize.min.js"></script>
    <style>
        nav .nav-wrapper {
            background-color: #26a69a;
        }
    </style>
</head>
<body>
    <div class="row">
        <nav>
            <div class="nav-wrapper">
            <a href="account" class="brand-logo">Home</a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
                <li><a href="customer">Settings</a></li>
                <li><a href="logout">Logout</a></li>
            </ul>
            </div>
        </nav>
        <div class="col s6 offset-s3">
            <h4>Accounts</h4>
            <ul class="collection">
                
                <li class="collection-item avatar">
                    <span class="title">Cuenta personal</span>
                    <p>ES000000000000000000 <br>
                    <span >€500</span>
                    </p>
                    <a href="statements/1" class="secondary-content"><i class="material-icons">info_outline</i></a>
                </li>
                
                <li class="collection-item avatar">
                    <span class="title">Cuenta ahorro</span>
                    <p>ES111111111111111111 <br>
                    <span >€8000</span>
                    </p>
                    <a href="statements/2" class="secondary-content"><i class="material-icons">info_outline</i></a>
                </li>
                
            </ul>
        </div>
    </div>
</body>
</html>
"""

statement_1_html = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
    <title>Statements</title>

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/js/materialize.min.js"></script>
    <style>
        nav .nav-wrapper {
            background-color: #26a69a;
        }
    </style>
</head>
<body>
    <div class="row">
        <nav>
            <div class="nav-wrapper">
            <a href="/account" class="brand-logo">Home</a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
                <li><a href="/customer">Settings</a></li>
                <li><a href="/logout">Logout</a></li>
            </ul>
            </div>
        </nav>
        <div class="col s6 offset-s3">
            <table class="striped">
                <thead>
                    <tr>
                        <th>Statement</th>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>
                    
                    <tr>
                        <td>La Beba</td>
                        <td>24/07/2021</td>
                        <td class="red-text text-darken-2">€30</td>
                        <td >€400</td>
                    </tr>
                    
                    <tr>
                        <td>Transferencia</td>
                        <td>15/06/2021</td>
                        <td >€100</td>
                        <td >€500</td>
                    </tr>
                    
                    <tr>
                        <td>Amazon</td>
                        <td>02/06/2018</td>
                        <td class="red-text text-darken-2">€20</td>
                        <td >€282</td>
                    </tr>
                    
                    <tr>
                        <td>Transferencia</td>
                        <td>11/05/2021</td>
                        <td >€80</td>
                        <td >€700</td>
                    </tr>
                    
                    <tr>
                        <td>Netflix</td>
                        <td>01/04/2021</td>
                        <td class="red-text text-darken-2">€30</td>
                        <td >€999</td>
                    </tr>
                    
                    <tr>
                        <td>Bar Pepe</td>
                        <td>03/01/2021</td>
                        <td class="red-text text-darken-2">€30</td>
                        <td >€111</td>
                    </tr>
                    
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

statement_2_html = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
    <title>Statements</title>

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/js/materialize.min.js"></script>
    <style>
        nav .nav-wrapper {
            background-color: #26a69a;
        }
    </style>
</head>
<body>
    <div class="row">
        <nav>
            <div class="nav-wrapper">
            <a href="/account" class="brand-logo">Home</a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
                <li><a href="/customer">Settings</a></li>
                <li><a href="/logout">Logout</a></li>
            </ul>
            </div>
        </nav>
        <div class="col s6 offset-s3">
            <table class="striped">
                <thead>
                    <tr>
                        <th>Statement</th>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>
                    
                    <tr>
                        <td>McDonalds</td>
                        <td>25/07/2018</td>
                        <td class="red-text text-darken-2">€12</td>
                        <td >€1322.2</td>
                    </tr>
                    
                    <tr>
                        <td>Nomina</td>
                        <td>21/07/2018</td>
                        <td >€280</td>
                        <td >€1334.2</td>
                    </tr>
                    
                    <tr>
                        <td>Nomina</td>
                        <td>12/02/2018</td>
                        <td >€280</td>
                        <td >€1054.2</td>
                    </tr>
                    
                    <tr>
                        <td>Compra online</td>
                        <td>01/01/2018</td>
                        <td class="red-text text-darken-2">€20</td>
                        <td >€774.2</td>
                    </tr>
                    
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""


def test_unnax_login() -> None:
    ws = Scraping("Y3216434F", "pperez2018")
    cookie_session = ws.login()
    assert cookie_session != "Problem getting data from https://test.unnax.com/"


def process_customer_data() -> int:
    ws = Scraping("Y3216434F", "pperez2018")
    ws.get_customer()
    data = ws.data.get("customer")
    return data


@responses.activate
def test_mocked_customer_data_extraction() -> None:
    responses.add(
        responses.GET,
        "https://test.unnax.com/customer",
        body=customer_html,
        status=200,
    )
    data = process_customer_data()
    assert data.get("name") == "Jose Garcia"
    assert data.get("phone") == "+18498123123"
    assert data.get("email") == "jgarcia@mail.com"
    assert data.get("address") == "Santo Domingo, Av 27 de Febrero #45"


def process_accounts_statements_data() -> int:
    ws = Scraping("Y3216434F", "pperez2018")
    ws.get_accounts_statements()
    data = ws.data.get("accounts")
    return data


@responses.activate
def test_mocked_accounts_statements_extraction() -> None:
    responses.add(
        responses.GET,
        "https://test.unnax.com/account",
        body=account_html,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://test.unnax.com/statements/1",
        body=statement_1_html,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://test.unnax.com/statements/2",
        body=statement_2_html,
        status=200,
    )
    data = process_accounts_statements_data()
    for ac in data:
        if ac.get("number") == "ES000000000000000000":
            assert ac.get("name") == "Cuenta personal"
            assert ac.get("currency") == "EUR"
            assert ac.get("balance") == "500"
            assert len(ac.get("statements")) == 6
            for st in ac.get("statements"):
                if st.get("date") == "2021-07-24":
                    assert st.get("date") == "2021-07-24"
                    assert st.get("amount") == "-30"
                    assert st.get("balance") == "400"
                    assert st.get("concept") == "La Beba"
                if st.get("date") == "2021-06-15":
                    assert st.get("date") == "2021-06-15"
                    assert st.get("amount") == "100"
                    assert st.get("balance") == "500"
                    assert st.get("concept") == "Transferencia"
                if st.get("date") == "2018-06-02":
                    assert st.get("date") == "2018-06-02"
                    assert st.get("amount") == "-20"
                    assert st.get("balance") == "282"
                    assert st.get("concept") == "Amazon"
                if st.get("date") == "2021-05-11":
                    assert st.get("date") == "2021-05-11"
                    assert st.get("amount") == "80"
                    assert st.get("balance") == "700"
                    assert st.get("concept") == "Transferencia"
                if st.get("date") == "2021-04-01":
                    assert st.get("date") == "2021-04-01"
                    assert st.get("amount") == "-30"
                    assert st.get("balance") == "999"
                    assert st.get("concept") == "Netflix"
                if st.get("date") == "2021-01-03":
                    assert st.get("date") == "2021-01-03"
                    assert st.get("amount") == "-30"
                    assert st.get("balance") == "111"
                    assert st.get("concept") == "Bar Pepe"
        if ac.get("number") == "ES111111111111111111":
            assert ac.get("name") == "Cuenta ahorro"
            assert ac.get("currency") == "EUR"
            assert ac.get("balance") == "8000"
            assert len(ac.get("statements")) == 4
            for st in ac.get("statements"):
                if st.get("date") == "2018-07-25":
                    assert st.get("date") == "2018-07-25"
                    assert st.get("amount") == "-12"
                    assert st.get("balance") == "1322.2"
                    assert st.get("concept") == "McDonalds"
                if st.get("date") == "2018-07-21":
                    assert st.get("date") == "2018-07-21"
                    assert st.get("amount") == "280"
                    assert st.get("balance") == "1334.2"
                    assert st.get("concept") == "Nomina"
                if st.get("date") == "2018-02-12":
                    assert st.get("date") == "2018-02-12"
                    assert st.get("amount") == "280"
                    assert st.get("balance") == "1054.2"
                    assert st.get("concept") == "Nomina"
                if st.get("date") == "2018-01-01":
                    assert st.get("date") == "2018-01-01"
                    assert st.get("amount") == "-20"
                    assert st.get("balance") == "774.2"
                    assert st.get("concept") == "Compra online"