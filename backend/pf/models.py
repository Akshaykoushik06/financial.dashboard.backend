from djongo import models


class PFTransactionsModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100)
