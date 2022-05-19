from django.apps import apps
from django.test import TestCase
from app.wsgi import *
# Create your tests here.
from core.login.models import User

u = User()

u.controller.prueba()
u.controller.prueba()

print(u)