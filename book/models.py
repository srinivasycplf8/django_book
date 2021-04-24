from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.

class Book(models.Model):
    ISBN = models.BigIntegerField()
    title =  models.CharField(max_length=250)
    author =  models.CharField(max_length=250)
    publisher =  models.CharField(max_length=250)
    language =  models.CharField(max_length=50)
    publication_date =  models.DateField()
    number_of_pages =  models.PositiveIntegerField()
    number_of_books =   models.PositiveIntegerField()
    price =  models.PositiveIntegerField()
    keyword =  models.CharField(max_length=50)
    subject =  models.CharField(max_length=50)

    def __str__(self):

        return "Title name " + self.title
    



	

