from . import views
from django.conf.urls import  url, include
from rest_framework.urlpatterns import format_suffix_patterns





urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^customer/$', views.customer_list, name='customer_list'),
    url(r'^customer/(?P<pk>\d+)/delete/$', views.customer_delete, name='customer_delete'),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.customer_edit, name='customer_edit'),
    url(r'^customer/(?P<pk>\d+)/portfolio/$', views.portfolio, name='portfolio'),
    url(r'^customer/create/$', views.customer_new, name='customer_new'),
    url(r'^stock/$', views.stock_list, name='stock_list'),
    url(r'^stock/(?P<pk>\d+)/delete/$', views.stock_delete, name='stock_delete'),
    url(r'^stock/(?P<pk>\d+)/edit/$', views.stock_edit, name='stock_edit'),
    url(r'^stock/create/$', views.stock_new, name='stock_new'),
    url(r'^investment/$', views.investment_list, name='investment_list'),
    url(r'^investment/(?P<pk>\d+)/delete/$', views.investment_delete, name='investment_delete'),
    url(r'^investment/(?P<pk>\d+)/edit/$', views.investment_edit, name='investment_edit'),
    url(r'^investment/create/$', views.investment_new, name='investment_new'),
    url(r'^mutual_funds/$', views.mutual_funds_list, name='mutual_funds_list'),
    url(r'^mutual_funds/create/$', views.mutual_funds_new, name='mutual_funds_new'),
    url(r'^mutual_funds/(?P<pk>\d+)/delete/$', views.mutual_funds_delete, name='mutual_funds_delete'),
    url(r'^mutual_funds/(?P<pk>\d+)/edit/$', views.mutual_funds_edit, name='mutual_funds_edit'),
    # url(r'^customer/share/$', views.share, name='share'),
    url(r'^accounts/profile/$', views.home, name='home'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^customers_json/', views.CustomerList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)