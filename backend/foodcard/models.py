from djongo import models


class FoodCardTransactionsModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100)
    credit = models.BooleanField()
