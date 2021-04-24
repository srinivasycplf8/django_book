from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Book
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from django.db import connection


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