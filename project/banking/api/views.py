import requests
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import BankingData, Customer, Account
from .serializers import CustomerSerializer, AccountSerializer
from ..task import get_banking_data
from celery.result import AsyncResult

import logging

logger = logging.getLogger(__name__)


class ReadView(APIView):
    """View dedicated to extract and get data from http://test.unnax.com/"""

    def post(self, request, *args, **kwargs):
        try:
            bkd = BankingData.objects.create(code=kwargs["code"])
            response = {"status": bkd.status}
            username = request.data["username"]
            password = request.data["password"]
            task = get_banking_data.delay(username, password, kwargs["code"])
            task_result = AsyncResult(task.id)
            bkd.task_id = task.id
            bkd.save()
            logger.info(
                f"Task Created {task.id} {task_result.status} {task_result.result}"
            )
        except Exception as e:
            message = "Bad request, the search code must be unique"
            if "username" not in request.data or "password" not in request.data:
                message = "Username and password are required."
            logger.error(message)
            return Response({"message": message}, 400)
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

    def delete(self, request, **kwargs):
        bkd = get_object_or_404(BankingData, code=kwargs["code"])
        bkd.delete()
        return Response(status=204)