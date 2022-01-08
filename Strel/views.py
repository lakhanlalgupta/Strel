from django.shortcuts import render,redirect, HttpResponse
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import messages