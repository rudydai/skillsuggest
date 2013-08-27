from django.db import models

class User(models.Model):
#need to keep track of states and tokens
    name = models.CharField()
    state = models.CharField(max_length=30)
    token = models.CharField()
    expiry = models.DateTimeField()



# Create your models here.
