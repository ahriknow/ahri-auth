from django.urls import path
from . import views

urlpatterns = [
    path('jurisdiction/', views.JurManageView.as_view()),
    path('jurisdiction/<id>/', views.JurManageView.as_view()),
]
