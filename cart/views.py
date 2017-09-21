# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, FormView, TemplateView, View
from .mixin import LoginRequireMixin
from .models import Course, Purchase
from .shoppingcart import Cart

# Create your views here.


class CourseView(ListView):
    model = Course
    template_name = 'cart/courses_list.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        is_auth = False
        name = ""

        if self.request.user.is_authenticated():
            is_auth = True
            name = self.request.user.username

        context.update({'is_auth': is_auth, 'name': name})
        return context


class PurchaseView(LoginRequireMixin, ListView):
    model = Purchase
    template_name = 'cart/courses_cart.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PurchaseView, self).get_context_data(**kwargs)
        is_auth = False
        name = ""

        if self.request.user.is_authenticated():
            is_auth = True
            name = self.request.user.username

        context.update({'is_auth': is_auth, 'name': name})
        return context


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'cart/login.html'
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.user_cache)
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            if next_url:
                return redirect(next_url)
        return super(LoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        is_auth = False

        if self.request.user.is_authenticated():
            is_auth = True

        context.update({'is_auth': is_auth})
        return context

class LogoutView(View):
    def get(self, request):
        logout(request)
        if 'next' in request.GET:
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
        return redirect('courses')


class AddView(TemplateView):
    template_name = 'cart/courses_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        cart = Cart(request.session)
        course = Course.objects.get(id=self.kwargs.get('pk'))
        cart.add(course, price=course.price)
        return redirect('courses')


class DeleteView(LoginRequireMixin, TemplateView):
    template_name = 'cart/courses_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        cart = Cart(request.session)
        course = Course.objects.get(id=self.kwargs.get('pk'))
        cart.remove(course)
        return redirect('cart')


class BuyView(LoginRequireMixin, TemplateView):
    template_name = 'cart/courses_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        cart = Cart(request.session)
        cart_courses = cart.courses
        for course in cart_courses:
            purchase = Purchase()
            purchase.user = self.request.user
            purchase.course = course
            purchase.quantity = cart.quantity(course)
            purchase.save()

        cart.clear()
        return redirect('courses')
