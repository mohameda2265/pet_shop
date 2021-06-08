from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PetsAPI.as_view(), name='Create_Review_Pet'),
    path('<int:pet_id>', PetsAPI.as_view(), name='Update_Delete_Pet'),
    path('item/<int:pet_item_id>', PetItemAPI.as_view(), name='Update_Delete_Item_Pet'),
]
