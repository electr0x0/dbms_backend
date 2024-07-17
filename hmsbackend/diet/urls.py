# urls.py
from django.urls import path
from .views import DietCreateView

urlpatterns = [
    path('create-diet/', DietCreateView.as_view(), name='create-diet'),
]
