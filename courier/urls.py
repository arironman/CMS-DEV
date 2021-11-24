from django.urls import path
from courier import views


urlpatterns = [
    # basic urls
    path('', views.create_parcle, name='create_parcle'),
    path('<int:courier_id>/', views.courier),
    path('detail/<int:courier_id>/', views.detail_parcle, name='courier_detail'),
    path('cancel/<int:courier_id>/', views.cancel_parcle),
    path('conform/<int:courier_id>/', views.conform_parcle, name='conform_parcle'),
]
