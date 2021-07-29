from djongo import models


class ICICITransactionsModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100)
    credit = models.BooleanField()


class HDFCTransactionsModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100)
    credit = models.BooleanField()


class IOBTransactionsModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100)
    credit = models.BooleanField()


class CanaraTransactionsModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100)
    credit = models.BooleanField()
