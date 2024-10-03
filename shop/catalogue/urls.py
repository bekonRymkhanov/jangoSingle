from django.urls import path
from . import views

urlpatterns=[
    path('listItems/',views.listOfItems,name="list of items"),
    path('listItems/details/<int:id>', views.details, name='details'),
    path('', views.main, name='main'),

]

