from django.urls import include,path
from django.urls import path,re_path


"""online_book_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'book'

urlpatterns = [
    re_path(r'^$', views.index,name="index"),
    re_path(r'^order/$', views.order, name='order'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^feedback/$', views.feedback, name='feedback'),
    re_path(r'^detail/([0-9]+)/$', views.detail, name='detail'),
    re_path(r'^detail/([0-9]+)/([0-9]+)/$', views.detail, name='detail'),
    re_path(r'^vote/([0-9]+)$', views.vote, name='vote'),
    re_path(r'^addbok/$', views.addbok, name='addbok'),
    re_path(r'^updatecopies/$', views.updatecopies, name='updatecopies'),
    re_path(r'^customers_web/$', views.customers_web, name='customers_web'),
    re_path(r'book/add/$', views.BookCreate.as_view(), name='book-add'),
    re_path(r'^user_set_manager/$', views.user_set_manager, name='user_set_manager'),
    re_path(r'^user_remove_manager/$', views.user_remove_manager, name='user_remove_manager'),
    re_path(r'^userpage/(?P<username>\w+)/$',views.userpage, name='userpage'),
    re_path(r'^trusted_page/$',views.trusted_page, name='trusted_page'),
    re_path(r'^untrusted_page/$',views.untrusted_page, name='untrusted_page'),
    re_path(r'^statistics/$',views.statistics, name='statistics'),
    re_path(r'^statistics/([0-9]+)/$',views.statistics, name='statistics'),
    re_path(r'^order_information/$',views.order_information, name='order_information'),









]
