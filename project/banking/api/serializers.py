from rest_framework import serializers
from ..models import BankingData, Customer, Account, Statement


class BankingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankingData
        fields = ["code", "status", "duration"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "name",
            "participation",
            "doc",
            "address",
            "email",
            "phone",
        ]


class StatementSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "date": value.date.strftime("%Y-%m-%d"),
            "amount": value.amount,
            "balance": value.balance,
            "concept": value.concept,
        }


class AccountSerializer(serializers.ModelSerializer):
    statements = StatementSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ["name", "number", "currency", "balance", "statements"]
