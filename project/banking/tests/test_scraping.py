import json, requests_mock, responses, requests
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


def test_unnax_login() -> None:
    ws = Scraping("Y3216434F", "pperez2018")
    cookie_session = ws.login()
    assert cookie_session != "Problem getting data from https://test.unnax.com/"


# TODO Muck all the request and test the ws methods
@responses.activate
def test_mocked_dogecoin_api() -> None:
    responses.add(
        responses.POST,
        "https://test.unnax.com/login",
        body=login_html,
        status=200,
    )

    assert process_crypto() == True


def process_crypto() -> int:
    response = requests.post(
        url="https://test.unnax.com/login",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    response_content = response.text
    if response.status_code != 200:
        raise ValueError("Request to https://test.unnax.com/login failed")

    if "ES232100123303030032" in response_content:
        return True

    return False
