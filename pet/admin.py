from django.contrib import admin

from .models import *

admin.site.register(Pet)
admin.site.register(PetItem)
admin.site.register(Order)
admin.site.register(OrderItem)
