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
        query =  request.GET.get("q") 
        if query : 
            query = '%'+str(query)+'%'
            cursor.execute("select * from book_book where title LIKE '%s' or author LIKE '%s' or publisher Like '%s' or language LIKE '%s' ORDER by publication_date DESC; "%(query,query,query,query))
            columns = [col[0] for col in cursor.description]
            book_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        context={
        'all_books':book_list,
        'isManager':isManager
        }
        return render(request, 'book/index.html',context)

@login_required(login_url='/login')
def order_information(request):
    order_list = ""
    username = request.user.username
    with connection.cursor() as cursor:
        cursor.execute("select title,id from book_book where id in (select distinct(book_id) from book_order where customer_id='%s');"%(username))
        columns = [col[0] for col in cursor.description]
        order_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        context={
            'order_list':order_list
        }

    return render(request,'book/order_information.html',context)

        

@login_required(login_url='/login')
def statistics(request,author=0,publisher=0):
    popular_books=''
    popular_authors=''
    popular_publishers=''
    with connection.cursor() as cursor:
        if request.method == 'POST': 
            number_of_books=int(request.POST['statistics_id'])
            cursor.execute("select count(distinct(book_id)) from book_order;")
            different_books = int(cursor.fetchone()[0])
            if number_of_books>=different_books:
                sql = "select title,id from book_book where id in(select book_id from ( select book_id,count(*) from book_order group by book_id order by count(*) DESC)P)"
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                popular_books= [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                sql = "select title,id from book_book where id in(select book_id from ( select book_id,count(*) from book_order group by book_id order by count(*) DESC)P)"
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                popular_books= [dict(zip(columns, row)) for row in cursor.fetchall()][0:number_of_books]
            number_of_authors=int(request.POST['statistics_id'])
            cursor.execute(" select count(distinct(author)) from book_book where id in (select distinct(book_id) from book_order);")
            different_authors = int(cursor.fetchone()[0])
            if number_of_authors>=different_authors:
                sql = "select distinct(author) from book_book where id in(select book_id from ( select book_id,count(*) from book_order group by book_id order by count(*) DESC)P)"
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                popular_authors= [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                sql = "select distinct(author) from book_book where id in(select book_id from ( select book_id,count(*) from book_order group by book_id order by count(*) DESC)P)"
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                popular_authors= [dict(zip(columns, row)) for row in cursor.fetchall()][0:number_of_authors]
            
            number_of_publishers=int(request.POST['statistics_id'])
            cursor.execute(" select count(distinct(publisher)) from book_book where id in (select distinct(book_id) from book_order);")
            different_publishers = int(cursor.fetchone()[0])
            if number_of_publishers>=different_publishers:
                sql = "select distinct(publisher) from book_book where id in(select book_id from ( select book_id,count(*) from book_order group by book_id order by count(*) DESC)P)"
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                popular_publishers= [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                sql = "select distinct(publisher) from book_book where id in(select book_id from ( select book_id,count(*) from book_order group by book_id order by count(*) DESC)P)"
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                popular_publishers= [dict(zip(columns, row)) for row in cursor.fetchall()][0:number_of_publishers]

            
    
    return render(request,'book/statistics.html',{'popular_books':popular_books,'popular_authors':popular_authors,'popular_publishers':popular_publishers})

        

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
            out_of_stock=''
            stock=''
            less=''
            recommendation_list=''

            if availaible_copies>=copies:
                stock='1'
                username = request.user.username
                cursor.execute("INSERT INTO book_order (customer_id,book_id,order_date,order_status) \
                    VALUES ('%s','%s','%s','completed')"%(username,book_id,date))
                cursor.execute("UPDATE book_book SET number_of_books='%d' WHERE id = '%s' "%(availaible_copies-copies,book_id))
                cursor.execute("select title,id from book_book where id in (select distinct(book_id )from book_order where book_id!='%s' and customer_id in (select customer_id from book_order where book_id in ( select book_id from (select book_id from book_order where customer_id = '%s' GROUP BY book_id )P where customer_id!='%s')));"%(book_id,username,username))
                columns = [col[0] for col in cursor.description]
                recommendation_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
            elif availaible_copies==0 :
                out_of_stock='0'
            else:
                less='1'
                
            
    
    return render(request,'book/finished.html',{'out_of_stock':out_of_stock,'stock':stock,'less':less,'recommendation_list':recommendation_list})

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





