from django.urls import path
from user import views


urlpatterns = [
    # basic urls
    path('', views.user, name='user'),
]
