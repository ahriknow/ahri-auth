from django.urls import path
from . import views

urlpatterns = [
    path('department/', views.DeptManageView.as_view()),
    path('department/<id>/', views.DeptManageView.as_view()),
]
