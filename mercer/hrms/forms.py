# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets  # 插件
from django.forms import fields  # 字段


class LoginForm(forms.Form):
    uid = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'uid', 'placeholder': 'Username'}))
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': 'Password'}))


class RegisterForm(forms.Form):
    uid = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'uid', 'placeholder': 'Username'}))
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': 'Password'}))
    eml = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'eml', 'placeholder': 'Email'}))
    cname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cname', 'placeholder': 'Cname'}))
    cad = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cad', 'placeholder': 'Caddress'}))

class EmployeeForm(forms.Form):
    enumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'enumber', 'placeholder': 'number'}))
    ename = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'ename', 'placeholder': 'name'}))
    # edepartment = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'department', 'placeholder': 'epartment'}))
    #erank = forms.MultipleChoiceField(
        #widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'rank', 'placeholder': 'rank'}))
    # ejoin_date = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'join_date', 'placeholder': 'join_date'}))
