# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import BankingData, Customer, Account, Statement


@admin.register(BankingData)
class BankingDataAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "status", "created", "modified")
    list_filter = ("status", "created", "modified")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "banking_data",
        "name",
        "doc",
        "email",
        "phone",
        "participation",
        "address",
        "created",
        "modified",
    )
    list_filter = ("created", "modified", "banking_data")
    search_fields = ("name",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number",
        "name",
        "customer",
        "currency",
        "balance",
        "created",
        "modified",
    )
    list_filter = ("currency", "customer", "created", "modified")
    search_fields = ("name", "number")


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "amount",
        "balance",
        "concept",
        "date",
        "created",
        "modified",
    )
    list_filter = ("date", "account", "created", "modified")
