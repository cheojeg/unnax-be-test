from .models import BankingData, Customer, Account, Statement
from .scripts import Scraping


class WSUNNAX(Scraping):
    def save_data(self, code):
        bkd = BankingData.objects.get(code=code)
        customer = Customer.objects.create(banking_data=bkd, **self.data["customer"])
        for ac in self.data["accounts"]:
            statements = ac.pop("statements")
            account = Account.objects.create(**ac, customer=customer)
            Statement.objects.bulk_create(
                [Statement(**s, account=account) for s in statements]
            )
        bkd = BankingData.objects.get(code=code)
        bkd.status = "DONE"
        bkd.save()

    def __str__(self) -> str:
        return f"WSUNNAX: {self.username} - {self.password}"