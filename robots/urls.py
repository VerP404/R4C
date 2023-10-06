from django.urls import path
from . import views

urlpatterns = [
    path('api/created_robot/', views.CreatedRobotView.as_view(), name='created-robot'),
]
