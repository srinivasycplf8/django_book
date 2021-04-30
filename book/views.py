from django.db.models import query
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Book,Customer
from .forms import CustomerCreationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import connection
from django.contrib.auth import login,logout,authenticate
from django.template import RequestContext, context
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import CustomerCreationForm
from django.contrib.auth.models import User
import datetime
import ast
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView



@login_required(login_url='/login')
def index(request):
    book_list = ""
    with connection.cursor() as cursor:
        cursor.execute("select * from book_book")
        columns = [col[0] for col in cursor.description]
        book_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        username = request.user.username
        isManager = request.user.is_superuser
        context={
        'all_books':book_list,
        'isManager':isManager
        }
       
        
    return render(request, 'book/index.html',context)

@login_required(login_url='/login')
def customers_web(request):
    customer_list = ""
    with connection.cursor() as cursor:
        cursor.execute("select * from book_customer")
        columns = [col[0] for col in cursor.description]
        customer_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        username = request.user.username
        context={
        'all_customers':customer_list,
        }
       
        
    return render(request,'book/customers_web.html',context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('book:index')
        else:
            return HttpResponse("Username/Passoword incorrect")
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
            address = request.POST['address']
            card = request.POST['card']
            phone = request.POST['phone']
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
    with connection.cursor() as cursor:
        if request.method=='POST':
            now=datetime.datetime.now()
            date="%s/%s/%s" % (now.year, now.month, now.day)
            book_id = request.POST['order_isbn']
            copies = int(request.POST['order_copies'])  
            cursor.execute("SELECT number_of_books FROM book_book WHERE id = '%s'"%(book_id))
            availaible_copies = int(cursor.fetchone()[0])  
            if availaible_copies>=copies:
                username = request.user.username
                cursor.execute("INSERT INTO book_order (customer_id,book_id,order_date,order_status) \
                    VALUES ('%s','%s','%s','completed')"%(username,book_id,date))
                cursor.execute("UPDATE book_book SET number_of_books='%d' WHERE ISBN = '%s' "%(availaible_copies-copies,book_id))
                
            
    
    return render(request,'book/finished.html')

@login_required(login_url='/login')
def detail(request, isbn,useful=0):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM book_book WHERE id='%s';"%(isbn))
        columns = [col[0] for col in cursor.description]
        book = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if useful==0:
            cursor.execute("SELECT * FROM book_feedback WHERE book_id='%s';"%(isbn))
            columns = [col[0] for col in cursor.description]
            feedback_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        else:
            if request.method=='POST':
                selected_useful = int(request.POST['useful_id'])    
                sql =  "select count(*) from book_feedback where book_id='%s'"%(isbn)
                cursor.execute(sql)
                z = (cursor.fetchone()[0])
                count = int(z)
                if selected_useful >= count:
                    sql="select customer_id,book_id,score,text,rate from book_rating,book_feedback where isbn_id='%s' and book_id='%s' and rate>=1 GROUP by customer_id ORDER by rate DESC "%(isbn,isbn)
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    feedback_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    sql="select customer_id,book_id,score,text,rate from book_rating,book_feedback where isbn_id='%s' and book_id='%s' and rate>=1 GROUP by customer_id ORDER by rate DESC "%(isbn,isbn)
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    feedback_list = [dict(zip(columns, row)) for row in cursor.fetchall()][0:selected_useful]

        
        
        return render(request,'book/detail.html',{'book':book[0],'feedback_list':feedback_list})

@login_required(login_url='/login')
def userpage(request, username):
    with connection.cursor() as cursor:
        cursor.execute("select * from book_feedback,book_book WHERE book_book.id=book_feedback.book_id AND customer_id = '%s' "%(username))
        columns = [col[0] for col in cursor.description]
        customer_feedback=[dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.execute("select count(*) from book_trusted WHERE person_who_receving_id = '%s' "%(username))
        count = int(cursor.fetchone()[0]) 
        if count!=0:
            cursor.execute("select AVG(trusted_score) AS average from book_trusted WHERE person_who_receving_id = '%s' "%(username))
            columns = [col[0] for col in cursor.description]
        # x = [dict(zip(columns, row)) for row in cursor.fetchall()]
            z = (cursor.fetchone()[0])
            avg = float(z) 
        else:
            avg =0


        context={'customer_feedback':customer_feedback,'username':username,'trusted_userscore':avg,'count':count}


    return render(request,'book/userpage.html',context)

@login_required(login_url='/login')
def user_set_manager(request):
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        username = request.POST['user_form']  
    
        sql = "UPDATE book_customer SET is_superuser='%d' WHERE username='%s'"%(1,username) 
        cursor.execute(sql)
    return redirect('/book')

@login_required(login_url='/login')
def user_remove_manager(request):
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        username = request.POST['user_form']  
    
        sql = "UPDATE book_customer SET is_superuser='%d' WHERE username='%s'"%(0,username) 
        cursor.execute(sql)
    return redirect('/book')
        



@login_required(login_url='/login')
def feedback(request):
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        text = request.POST['feedback_text']
        ISBN = request.POST['feedback_isbn']
        score = request.POST['rating']
        username = request.user.username
        sql = "INSERT INTO book_feedback (text,score,book_id,customer_id) VALUES ('%s','%s','%s','%s')"%\
                (text,score,ISBN,username)
        cursor.execute(sql)
    return redirect('/book/detail/'+ISBN)


@login_required(login_url='/login')
def trusted_page(request):
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        t_score = int(request.POST['trusted_score'])
        u_score = 0
        voted_user = request.POST['user_trusted']
        username =  request.user.username

        if voted_user!=username:
            check = "select count(*) from book_trusted where person_who_receving_id='%s' and person_voted='%s'"%(voted_user,username)
            cursor.execute(check)
            z = (cursor.fetchone()[0])
            count = float(z)
            if count==0:
                sql = "INSERT INTO book_trusted (person_voted,person_who_receving_id,trusted_score,untrusted_score) VALUES ('%s','%s','%s','%s')"%\
                    (username,voted_user,t_score,u_score)
                cursor.execute(sql)
            else:
                return HttpResponse("u r not allowed to vote twice")
        else:
            return HttpResponse("u r not allwed to vote yourself")
        
    return redirect('/book/userpage/'+voted_user)

@login_required(login_url='/login')
def untrusted_page(request):
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        t_score = 0
        u_score = int(request.POST['untrusted_score'])
        username = request.user.username
        voted_user = request.POST['user_untrusted']
        if voted_user!=username:
            check = "select count(*) from book_trusted where person_who_receving_id='%s' and person_voted='%s'"%(voted_user,username)
            cursor.execute(check)
            z = (cursor.fetchone()[0])
            count = float(z)
            if count==0:
                sql = "INSERT INTO book_trusted (person_voted,person_who_receving_id,trusted_score,untrusted_score) VALUES ('%s','%s','%s','%s')"%\
                    (username,voted_user,t_score,u_score)
                cursor.execute(sql)
            else:
                return HttpResponse("u r not allowed to vote twice")
        else:
            return HttpResponse("u r not allwed to vote yourself")
        
    return redirect('/book/userpage/'+voted_user)

@login_required(login_url='/login')
def topuseful(request,isbn):
    if request.method=='POST':
        with connection.cursor() as cursor:
            requested_comments = int(request.POST['useful_id']) 
            sql =  "select count(*) from book_rating where isbn_id='%s'"%(isbn)
            cursor.execute(sql)
            z = (cursor.fetchone()[0])
            count = int(z)
            if requested_comments > count:
                sql =  "select * from book_rating where isbn_id='%s'"%(isbn)






@login_required(login_url='/login')
def vote(request,isbn):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            username=request.user.username
            score = request.POST['vote_score']
            user_rater = request.POST['vote_rater']
            feedback_id = request.POST['vote_feedback_id']
            username = request.user.username
            if username != user_rater :
                sql = "select count(*) from book_rating where feedback_id='%s' and rater='%s'"%(feedback_id,username)
                cursor.execute(sql)
                z = (cursor.fetchone()[0])
                count = float(z)
                if count==0:

                    sql = "INSERT INTO book_rating  (rater,rate,feedback_id,isbn_id,user_id) VALUES('%s','%s','%s','%s','%s')"%(username,score,feedback_id,isbn,user_rater)
                    cursor.execute(sql)
                    return redirect("/book/detail/"+isbn)
                else:
                   return HttpResponse("You cannot vote twice!")

               
               
            else:
                return HttpResponse("You cannot vote for yourself!")

class BookCreate(CreateView):
    model = Book
    fields = ['ISBN','title','author','publisher','language','publication_date','number_of_pages','number_of_books','price','keyword','subject']

@login_required(login_url='/login')
def addbok(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            ISBN= request.POST['ISBN']
            title= request.POST['title']
            author= request.POST['author']
            publisher= request.POST['publisher']
            language= request.POST['language']
            publication_date= request.POST['publication_date']
            number_of_pages= request.POST['number_of_pages']
            number_of_books= request.POST['number_of_books']
            price= request.POST['price']
            keyword= request.POST['keyword']
            subject= request.POST['subject']
            sql = "INSERT INTO book_book (ISBN,title,author,publisher,language,publication_date,number_of_pages,number_of_books,price,keyword,subject) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"\
            %(ISBN,title,author,publisher,language,publication_date,number_of_pages,number_of_books,price,keyword,subject)
            cursor.execute(sql) 
    
    return redirect('/book')

@login_required(login_url='/login')
def updatecopies(request):
    if request.method=='POST':
        with connection.cursor() as cursor:
            ISBN = request.POST['u_isbn']
            new_copies = int(request.POST['add_copies'])
            cursor.execute("SELECT number_of_books FROM book_book WHERE ISBN = '%s'"%(ISBN))
            available_books = int(cursor.fetchone()[0]) 
            cursor.execute("UPDATE book_book SET number_of_books='%d' WHERE ISBN='%s'"%(available_books+new_copies,ISBN)) 
            return redirect('/book')







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