from django.contrib import admin
from .models import *


class CatogeryAdmin(admin.ModelAdmin):
    list_display =('name', 'image', 'description')

admin.site.register(Product)
admin.site.register(Catogory, CatogeryAdmin)



# Register your models here.
