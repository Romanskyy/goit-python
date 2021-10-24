from django.db import models


# Create your models here
class Income(models.Model):
    amount = models.FloatField()
    comment = models.TextField(max_length=200, blank=True)
    date_of_deposit = models.DateTimeField()

    def __str__(self):
        return f'{self.date_of_deposit}, {self.amount}, {self.comment}'

    # rename table name to one you chose
    class Meta:
        db_table = 'incomes_table'


class Spending(models.Model):
    category = models.CharField(max_length=50)
    expenses_amount = models.FloatField()
    expenses_comment = models.TextField(max_length=200, blank=True)
    date_of_expenses = models.DateTimeField()

    def __str__(self):
        return f'{self.date_of_expenses}, {self.category}, {self.expenses_amount}, {self.expenses_comment}'

    # rename table name to one you chose
    class Meta:
        db_table = 'expensis_table'
