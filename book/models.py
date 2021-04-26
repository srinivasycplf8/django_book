from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils import timezone


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



class CustomerManager(BaseUserManager):
    def create_user(self,username,password,fullname,phone,card,address):
        user = self.model(
            username = username,
            fullname = fullname,
            phone = phone,
            card= card,
            address = address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,fullname,phone,card,address):
        user = self.model(
            username = username,
            fullname = fullname,
            phone = phone,
            card= card,
            address = address,
        )
        user.is_staff = True
        user.is_superuser = True 
        user.set_password(password)
        user.save(using=self._db)
        return user

    
class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True,primary_key=True)
    fullname = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    card = models.BigIntegerField()
    address = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname','phone','card','address']
    objects = CustomerManager()

class Order(models.Model):
    order_date = models.DateField(default=timezone.now)
    order_status = models.CharField(max_length=10,
        choices = (('submitted', 'submitted'),('executed', 'executed'),))
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    def __str__(self):
        return self.customer.fullname + " ordered the book " + self.book.title + "on this date "+self.order_date

	

