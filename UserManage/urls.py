from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserManageView.as_view()),
    path('user/<id>/', views.UserManageView.as_view()),
]
