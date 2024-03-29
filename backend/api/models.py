# from django.db import models
from djongo import models

# Create your models here.


class Todo(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title


class HomePageModel(models.Model):
    _id = models.ObjectIdField()
    icici_balance = models.DecimalField(max_digits=10, decimal_places=2)
    hdfc_balance = models.DecimalField(max_digits=10, decimal_places=2)
    iob_balance = models.DecimalField(max_digits=10, decimal_places=2)
    canara_balance = models.DecimalField(max_digits=10, decimal_places=2)
    liabilities_creditCardAmount = models.DecimalField(
        max_digits=10, decimal_places=2)
    foodCardBalance = models.DecimalField(max_digits=10, decimal_places=2)
