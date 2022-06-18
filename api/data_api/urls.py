from django.urls import path, include
from . import views


urlpatterns = [
    path('get-data/', views.get_data)
]
