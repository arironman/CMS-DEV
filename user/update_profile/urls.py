from django.urls import path
from user.update_profile import views


urlpatterns = [
    # user data update
    # path('verify_username/', views.verify_username, name='verify_username'),
    # path('verify_email/', views.verify_email, name='update_verify_email'),
    path('username/', views.username, name='update_username'),
    path('name/', views.name, name='update_name'),
    path('gender/', views.gender, name='update_gender'),
    path('email/', views.email, name='update_email'),
    path('mobile/', views.mobile, name='update_mobile'),

    # # user address update
    path('house_no/', views.house_number, name='update_house_no'),
    path('street/', views.street, name='update_street'),
    path('city/', views.city, name='update_city'),
    path('district/', views.district, name='update_district'),
    path('state/', views.state, name='update_state'),
    path('pincode/', views.pincode, name='update_pincode'),
    
]
