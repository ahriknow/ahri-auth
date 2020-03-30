from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginManageView.as_view()),
    path('userinfo/<id>/', views.LoginManageView.as_view()),
]
