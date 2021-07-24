import requests
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from ..models import BankingData
from ..models import Customer, Account, Statement
from .serializers import CustomerSerializer, StatementSerializer, AccountSerializer
from ..scripts import Scraping
from ..task import create_task
from celery.result import AsyncResult


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


class ReadView(APIView):
    """View dedicated to extract and get data from http://test.unnax.com/"""

    def post(self, request, *args, **kwargs):
        try:
            bkd = BankingData.objects.create(code=kwargs["code"])
            response = {"status": bkd.status}
            username = request.data["username"]
            password = request.data["password"]
            task = create_task.delay(username, password, kwargs["code"])
        except Exception as e:
            return Response(
                {"message": "Bad request, the search code must be unique"}, 400
            )
        return Response(response, 201)

    def get(self, request, **kwargs):
        bkd = get_object_or_404(BankingData, code=kwargs["code"])
        response = {"status": bkd.status}
        if bkd.status == "DONE":
            customer = Customer.objects.get(banking_data=bkd.id)
            accounts = Account.objects.filter(customer=customer)
            data = {
                "customer": CustomerSerializer(instance=customer).data,
                "accounts": [AccountSerializer(instance=ac).data for ac in accounts],
            }
            response["data"] = data
        if bkd.status == "ERROR":
            return Response({"message": "The data extraction has fail"}, 500)
        return Response(response)