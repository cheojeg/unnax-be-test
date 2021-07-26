import json
import requests
from bs4 import BeautifulSoup


class Scraping:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.data = {
            "customer": {},
            "accounts": [],
        }
        self.unnax_base_url = "https://test.unnax.com/"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.currencies = {
            "€": "EUR",
            "$": "USD",
            "¥": "JPY",
        }

    def login(self):
        doc = self.username
        password = self.password
        response = requests.Session()
        payload = f"password={password}&username={doc}"
        url = f"{self.unnax_base_url}login"
        try:
            response = response.post(url, headers=self.headers, data=payload)
            cookies = response.request.headers.get("Cookie")
            self.headers["Cookie"] = cookies
        except Exception as e:
            return False
        return cookies

    def get_customer(self):
        try:
            url = f"{self.unnax_base_url}customer"
            response = requests.request("GET", url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            customer_name = soup.find_all("li", {"class": "collection-header"})
            self.data["customer"]["name"] = customer_name[0].text
            customer_data = soup.find_all("li", {"class": "collection-item"})
            self.data["customer"]["phone"] = customer_data[0].text.replace(" ", "")
            self.data["customer"]["email"] = customer_data[1].text
            self.data["customer"]["address"] = customer_data[2].text
            self.data["customer"]["doc"] = self.username
            self.data["customer"]["participation"] = "Titular"
        except Exception as e:
            return False
        return True

    def get_accounts_statements(self):
        url = f"{self.unnax_base_url}account"
        html_accounts = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(html_accounts, "html.parser")
        accounts = soup.find_all("li", {"class": "collection-item avatar"})
        for ac in accounts:
            ac_balance = ac.find("p").text.replace("\n", "").split(" ")
            number = ac_balance[0]
            currency = self.currencies.get(ac_balance[1][0], ac_balance[1][0])
            balance = ac_balance[1][1:]
            name = ac.find("span", {"class": "title"}).text
            account = {
                "name": name,
                "number": number,
                "currency": currency,
                "balance": balance,
                "statements": [],
            }
            statements_url = ac.find("a")["href"]
            try:
                # Get the staments of each account
                response = requests.request(
                    "GET",
                    f"{self.unnax_base_url}{statements_url}",
                    headers=self.headers,
                )
                soup = BeautifulSoup(response.text, "html.parser")
                account_statements = [
                    x.find_all("td") for x in soup.find_all("tbody")[0].find_all("tr")
                ]
                for bba in account_statements:
                    date_base = bba[1].text
                    date = date_base[6:] + "-" + date_base[3:5] + "-" + date_base[:2]
                    amount = (
                        bba[2].text[1:]
                        if not bba[2].get("class")
                        else f"-{bba[2].text[1:]}"
                    )
                    balance = (
                        bba[3].text[1:]
                        if not bba[3].get("class")
                        else f"-{bba[3].text[1:]}"
                    )
                    concept = bba[0].text
                    statement = {
                        "date": date,
                        "amount": amount,
                        "balance": balance,
                        "concept": concept,
                    }
                    account["statements"].append(statement)
                self.data["accounts"].append(account)
            except:
                return False
        return True

    def read_data(self):
        # Get customer data
        cookie = self.login()
        customer = self.get_customer()
        ac_st = self.get_accounts_statements()
        if cookie != False and customer == True and ac_st == True:
            return "OK"
        else:
            return f"Problem getting data {cookie} {customer} {ac_st}"

    def print_data(self):
        doc = self.username
        password = self.password
        unnax_base_url = "https://test.unnax.com/"
        response = requests.Session()
        payload = f"password={password}&username={doc}"
        url = f"{unnax_base_url}login"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = response.post(url, headers=headers, data=payload)
        cookies = response.request.headers.get("Cookie")

        # Get customer data
        url = f"{unnax_base_url}customer"
        headers["Cookie"] = cookies
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        customer_name = soup.find_all("li", {"class": "collection-header"})
        customer_name = customer_name[0].text
        customer_data = soup.find_all("li", {"class": "collection-item"})
        customer_phone = customer_data[0].text
        customer_email = customer_data[1].text
        customer_address = customer_data[2].text
        currencies = {
            "€": "EUR",
            "$": "USD",
            "¥": "JPY",
        }
        url = f"{unnax_base_url}account"
        html_accounts = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_accounts, "html.parser")
        accounts = soup.find_all("li", {"class": "collection-item avatar"})
        total_accounts = len(accounts)
        print("# Resultado Ex:")
        print(f"Accounts ( {total_accounts} )")
        for ac in accounts:
            ac_balance = ac.find("p").text.replace("\n", "").split(" ")
            account_number = ac_balance[0]
            currency = currencies.get(ac_balance[1][0], ac_balance[1][0])
            account_balance = ac_balance[1][1:]
            account_name = ac.find("span", {"class": "title"}).text
            account_statements_url = ac.find("a")["href"]
            print("    Account Data:")
            print(f"        Name: {account_name}")
            print(f"        Number: {account_number}")
            print(f"        Currency: {currency}")
            print(f"        Balance: {account_balance}")
            print("")
            print("    Total customers: 1")
            print("        Customer Data:")
            print(f"            Name: {customer_name}")
            print("            Participation: Titular")
            print(f"            Doc: {doc}")
            print(f"            Address: {customer_address}")
            print(f"            Emails: {customer_email}")
            print(f"            Phones: {customer_phone}")
            print("")
            # Get the staments of each account
            response = requests.request(
                "GET",
                f"{unnax_base_url}{account_statements_url}",
                headers={"Cookie": cookies},
            )
            soup = BeautifulSoup(response.text, "html.parser")
            account_statements = [
                x.find_all("td") for x in soup.find_all("tbody")[0].find_all("tr")
            ]
            print(f"    Statements ( {len(account_statements)} )")
            print(f"        Date    |    Amount    |    Balance    |    Concept    ")
            for bba in account_statements:
                date_base = bba[1].text
                date = date_base[6:] + "-" + date_base[3:5] + "-" + date_base[:2]
                date = "    " + date.center(12) + "|"
                amount = (
                    bba[2].text[1:]
                    if not bba[2].get("class")
                    else f"-{bba[2].text[1:]}"
                )
                amount = amount.center(13) + "|"
                balance = (
                    bba[3].text[1:]
                    if not bba[3].get("class")
                    else f"-{bba[3].text[1:]}"
                )
                balance = balance.center(14) + "|"
                print(f"{date} {amount} {balance} {bba[0].text}")
            print("")