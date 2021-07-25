from djongo import models

choices = [
    ('debit', 'You spent on credit card'),
    ('credit', 'Money came back to credit card'),
    ('bill', 'Bill Payment')
]


class CreditCardTransactionsModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100)
    billPaid = models.BooleanField()
    type_of_txn = models.CharField(max_length=10, choices=choices)
