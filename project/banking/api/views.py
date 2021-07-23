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

# from ..models import Sundae, Syrup
# from .serializers import SundaeSerializer, SyrupSerializer


class WSUNNAX(Scraping):
    def save_data(self, bkd):
        customer = Customer.objects.create(banking_data=bkd, **self.data["customer"])
        for ac in self.data["accounts"]:
            statements = ac.pop("statements")
            account = Account.objects.create(**ac, customer=customer)
            Statement.objects.bulk_create(
                [Statement(**s, account=account) for s in statements]
            )

    def __str__(self) -> str:
        return f"WSUNNAX: {self.username} - {self.password}"


class ReadView(APIView):
    """View dedicated to extract and get data from http://test.unnax.com/"""

    def post(self, request, *args, **kwargs):
        try:
            bkd = BankingData.objects.create(code=kwargs["code"])
            status = 202
            response = {"status": bkd.status}
            username = request.data["username"]
            password = request.data["password"]
            print("antes de llamar al task")
            ws = WSUNNAX(username, password)
            task = create_task(ws, bkd)
        except Exception as e:
            print(e)
            status = 400
            response = {"message": "Bad request, the search code must be unique"}
        return Response(response, status)

    def get(self, request, **kwargs):
        try:
            bkd = get_object_or_404(BankingData, code=kwargs["code"])
            response = {"status": bkd.status}
            status = 200
            if bkd.status == "DONE":
                customer = Customer.objects.get(banking_data=bkd.id)
                accounts = Account.objects.filter(customer=customer)
                data = {
                    "customer": CustomerSerializer(instance=customer).data,
                    "accounts": [
                        AccountSerializer(instance=ac).data for ac in accounts
                    ],
                }
                response["data"] = data
            if bkd.status == "ERROR":
                response["message"] = "The data extraction has fail"
                status = 500
        except Exception:
            response = {"message": "Has occurred an error processing the response"}
            status = 500
        return Response(response, status)

        # sundae = get_object_or_404(Sundae, uuid=request.data['uuid'])
        # try:
        #     sundae.add_syrup(request.data['syrup'])
        # except Sundae.TooManySyrups:
        #     msg = "Sundae already maxed out for syrups"
        #     return Response({'message': msg}, status_code=400)
        # except Syrup.DoesNotExist
        #     msg = "{} does not exist".format(request.data['syrup'])
        #     return Response({'message': msg}, status_code=404)
        # return Response(SundaeSerializer(sundae).data)


# class BankginDataViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """

#     # serializer = CustomerSerializer
#     def list(self, request):
#         queryset = Customer.objects.all()
#         serializer = CustomerSerializer(queryset, many=True)
#         return Response({"data": serializer.data, "status": "gola"})
