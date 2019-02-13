from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.category





class Record(models.Model):

    BALANCE_TYPE = ((u'收入',u'收入'), (u'支出',u'支出'))
    date = models.DateField()
    description = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cash = models.IntegerField()
    balance_type = models.CharField(max_length = 2, choices=BALANCE_TYPE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL ,null=True)
    def __str__(self):
        return self.description