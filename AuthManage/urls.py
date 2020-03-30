from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.AuthManageView.as_view()),
    path('auth/<id>/', views.AuthManageView.as_view()),
]
