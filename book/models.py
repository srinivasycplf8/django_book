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
        user = self.model(username = username,fullname = fullname,card= card,address = address, phone = phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,fullname,phone,card,address):
        user = self.model(username = username,fullname = fullname,card= card,address = address,phone = phone
        )

        user.is_superuser = True 

        user.is_staff = True

        user.set_password(password)

        user.save(using=self._db)
        return user

    
class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True,primary_key=True)
    fullname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=100)

    phone = models.BigIntegerField()

    card = models.BigIntegerField()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['fullname','address','phone','card']

    objects = CustomerManager()

class Order(models.Model):
    order_date = models.DateField(default=timezone.now)
    order_status = models.CharField(max_length=54,choices = (('submitted', 'submitted'),('finishing', 'finishing'),))
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)


class Feedback(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(choices=((0, '0'),(1, '1'),(2, '2'),(4, '4'),(3, '3'),(5, '5'),(6, '6'),(7, '7'),(10, '10'),(9, '9'),(8, '8')))

class Rating(models.Model):
    rater = models.CharField(max_length=100)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback,on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    isbn = models.ForeignKey(Book,on_delete=models.CASCADE)


class Trusted(models.Model):
    person_who_receving = models.ForeignKey(Customer,on_delete=models.CASCADE)
    person_voted = models.CharField(max_length=100,default=None)
    trusted_score = models.PositiveIntegerField(default=0)
    untrusted_score = models.PositiveIntegerField(default=0)


	

