from django.urls import path
from general import views

urlpatterns = [
    # basic urls
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about-us/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_method, name='login'),
    path('logout/', views.logout_method, name='logout'),
    # path('user/', views.test, name='test'),
    
    # return the districts of given state
    path('district/', views.districts, name='districts'),
    path('pincode/', views.pincodes, name='pincodes'),

    # checking the avaibility of username and email
    path('username/', views.available_username, name='available_username'),
    path('email/', views.available_email, name='available_email'),


    # urls for forget password
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/<str:username>/<str:otp>',
         views.update_password, name='update_password'),

]
