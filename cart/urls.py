# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import CourseView, LoginView, PurchaseView, AddView, DeleteView, BuyView, LogoutView

urlpatterns = [
    url(r'^$', CourseView.as_view(), name='courses'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^cart/$', PurchaseView.as_view(), name='cart'),
    url(r'^cart/buy/$', BuyView.as_view(), name='buy'),
    url(r'^cart/(?P<pk>[^/]+)/add/$', AddView.as_view()),
    url(r'^cart/(?P<pk>[^/]+)/delete/$', DeleteView.as_view()),
    url(r'^cart/(?P<pk>[^/]+)/delete/$', DeleteView.as_view()),
]
