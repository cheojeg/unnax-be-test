from enum import unique
from django.db import models
from requests.models import codes

# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BankingData(TimeStampedModel):
    """Model definition for MODELNAME."""

    class States(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        DONE = "DONE", "DONE"
        ERROR = "ERROR", "ERROR"

    code = models.CharField(max_length=50, unique=True, db_index=True, default="")
    task_id = models.CharField(max_length=250, blank=True, null=True, default="")
    status = models.CharField(
        max_length=30, choices=States.choices, default=States.PENDING
    )

    class Meta:
        verbose_name = "Search Banking Data"
        verbose_name_plural = "Search Banking Data"

    def __str__(self):
        return self.code


class Customer(TimeStampedModel):

    name = models.CharField(max_length=80)
    participation = models.CharField(max_length=80)
    doc = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    banking_data = models.ForeignKey(BankingData, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.banking_data.code} - {self.name}"


class Account(TimeStampedModel):

    name = models.CharField(max_length=80)
    number = models.CharField(max_length=80)
    currency = models.CharField(max_length=5)
    balance = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Account"

    def __str__(self):
        return f"{self.customer.banking_data.code} - {self.number}"


class Statement(TimeStampedModel):
    date = models.DateField(auto_now=False, auto_now_add=False)
    amount = models.FloatField()
    balance = models.FloatField()
    concept = models.TextField()
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="statements"
    )

    class Meta:
        verbose_name = "Statement"
        verbose_name_plural = "Statements"

    def __str__(self):
        return f"{self.account.number} - {self.id}"
