from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Book,Customer
from .forms import CustomerCreationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import connection
from django.contrib.auth import login,logout,authenticate
from django.template import RequestContext
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import CustomerCreationForm
from django.contrib.auth.models import User
import datetime



@login_required(login_url='/login')
def index(request):
    book_list = ""
    with connection.cursor() as cursor:
        cursor.execute("select * from book_book")
        columns = [col[0] for col in cursor.description]
        book_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        context={
        'all_books':book_list
        }
        
    return render(request, 'book/index.html',context)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('book:index')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("You have entered wrong username or password.")
    else:
        return render(request, 'book/login.html')

def register(request):
    cur = connection.cursor()
    registered = False
    if request.method == 'POST':
        user_form = CustomerCreationForm(data=request.POST)
        if user_form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            fullname = request.POST['fullname']
            phone = request.POST['phone']
            card = request.POST['card']
            address = request.POST['address']
            sql = "INSERT INTO book_customer VALUES\
            ('password',NULL,'0','%s','%s','%s','%s','%s','1','1');"%(username,fullname,phone,card,address)
            cur.execute(sql) 
            u = Customer.objects.get(username=username)
            u.set_password("%s"% password)
            u.save()
            registered = True
        
    else:
        user_form = CustomerCreationForm()
    return render(request,'book/signup.html',{'user_form': user_form, 'registered': registered,'base_template':'templates/base.html'})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    
    return render(request, 'book/login.html')

def order(request):
    context = RequestContext(request)
    info = "Sorry, your request is invalid."
    if request.method == 'POST':
        ISBN = request.POST['order_isbn']
        title = request.POST['order_title']
        copies = int(request.POST['order_copies'])
        cur = connection.cursor()
        try:
            cur.execute("SELECT number_of_books FROM book_book WHERE ISBN = '%s'"%(ISBN))
            avail = int(cur.fetchone()[0])  
            if avail > 0:
                username = request.user.username
                now=datetime.datetime.now()
                date="%s/%s/%s" % (now.day, now.month, now.year) 
                cur.execute("INSERT INTO book_order (customer_id,book_id,order_date,order_status) VALUES ('%s','%s','%s','submitted')"%(username,ISBN,date))
                cur.execute("UPDATE book_book SET number_of_books='%d' WHERE ISBN='%s'"%(avail-copies,ISBN))
                info = "You have ordered "+title+" successfully."
            else:
                info = "Sorry, "+title+" is currently out of stock."
        except Book.DoesNotExist:
            info = "Please enter a valid ISBN."
    return HttpResponse(info)


'''
class DetailView(generic.DetailView):
    model=Album
    template_name='music/detail.html'

  
class AlbumCreate(CreateView):
    model=Album
    fields=['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model=Album
    fields=['artist','album_title','genre','album_logo']


class AlbumDelete(DeleteView):
    model=Album
    success_url=reverse_lazy('music:index')'''