from django.contrib import admin
from . models import *
# Register your models here.
models = [Department, Course, Holder, Certificate, Signature]

for model in models:
    admin.site.register(model)
