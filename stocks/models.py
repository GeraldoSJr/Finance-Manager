from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.


class Stock(models.Model):
    amount = models.FloatField()
    price = models.FloatField()
    date = models.DateField(default=now)
    ticker = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']
