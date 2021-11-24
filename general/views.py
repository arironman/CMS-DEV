from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from CMS.variables import *

# Importing Email Stuff here
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives, message
from random import randint
from django.utils.html import strip_tags
from CMS import settings


# Importing Models
from user.models import CustomUser as User
from user.models import UserAddress
from general.models import AvailableDestination
from user.update_profile.views import pincode
from CMS.destination import state as states



# Create your views here.
def home(request):
    '''
        Handle the home/index page
    '''

    title = 'Home | CMS'
    params = {'title':title}
    return render(request, 'general/home.html', params)

def about(request):
    '''
        Handling the request page
    '''
    title = 'About Us | CMS'
    params = {'title':title}
    return render(request, 'general/about.html', params)

def contact(request):
    '''
        Handle the contact us page\n
        Handle both POST and GET request\n
        In POST request, we are sending the mail to admin, but here first we have to add email and password to settings.py.

    '''

    # handling th POST request
    if request.method == 'POST':
        # fetching the data
        name = request.POST['name']
        email = request.POST['email']
        description = request.POST['description']
        user = request.user

        # sending the mail to the report
        email_params = {
            'name': name,
            'description': description,
            'user' : user,
            'email': email
            }

        mail_subject = 'CMS - Contact Us'
        html_content = render_to_string('general/contact_mail.html', email_params)
        text_content = strip_tags(html_content)
        to_email = 'Anuragrai15march@gmail.com'

        email_send = EmailMultiAlternatives(mail_subject, text_content, settings.EMAIL_HOST_USER, to=[to_email])
        email_send.attach_alternative(html_content, 'text/html')
        email_send.send()

        messages.error(request, 'Your Problem is successfully reported.')
        return redirect('home')

    # Handling the GET request
    title = 'Contact Us | CMS'
    params = {'title':title}
    return render(request, 'general/contact.html', params)


def auth_code_validation(request, username, code):
    '''
        Authenticate the activation url.\n
        Need to Update

    '''
    user = User.objects.get(otp=code, username=username)
    if user == None:
        messages.success(request, 'Please Create Account First.')
        return redirect('signup')

    else:
        user_detail.activation_code = '000000'
        user = user_detail.user
        user.is_active = True
        user_detail.save()
        user.save()
        messages.success(request, 'Account Created Successfully. Please login.')
        return redirect('home')
    

def signup(request):
    '''
        Handle the signup method.\n
        Handle both GET and POST request.\n
        Need to upadate
    '''

    # Handling the POST request
    if request.method == 'POST':
        username = request.POST['username'].lower()
        name = request.POST['name']
        name_list = name.split(' ')
        if len(name_list) > 1:
            last_name = name_list[-1]
            name_list.pop()
            first_name = ' '.join(name_list)
        else:
            first_name = name_list[0]
            last_name = ''

        email = request.POST['email'].lower()
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        password_1 = request.POST['password']
        password_2 = request.POST['conform-password']

        # fetching address
        house_number = request.POST['delivery-house-no']
        street = request.POST['delivery-street']
        city = request.POST['delivery-city']
        state = request.POST['delivery-state']
        district = request.POST['delivery-district']
        pincode = request.POST['delivery-pincode']



        # checking passwords
        if password_1 != password_2:
            messages.error(request, 'Oops, Password do not match. Try again!')
            return redirect('signup')
    
        # validating username
        if ' ' in username or username in NON_USERNAME_WORDS:
            messages.error(request, 'Invalid Username. Try again!')
            return redirect('signup')
    
        # checking data is not null
        if (username == '' or first_name=='' or email==''): 
            messages.error(request, 'Oops, Something went wrong. Try again!')
            return redirect('signup')
        
        # checking email is registered or not
        registered_email = User.objects.filter(email = email)
        if len(registered_email) > 0:
            messages.error(request, 'Oops, Email is already Registered. Please try with another email.')
            return redirect('signup')

        # creating user and user address
        try:
            user = User.objects.create_user(username, email, password_1)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True
            user.gender = gender
            user.dob = dob
            user.email = email
            user.mobile = mobile
            user.save()
            
            address = UserAddress(user=user, house_number=house_number, street=street, city=city, state=state, district=district, pincode=pincode)
            address.save()
            messages.error(request, 'Account Created Successfully.')
        except:
            messages.error(request, 'Oops, Something went wrong. Try Again!')
            return redirect('signup')
        
        return redirect('home')
        
    # Handling the GET request
    # Handling the GET request for authenticated user
    if request.user.is_authenticated:
        messages.success(request, "Please Log Out from your current Account to Create New Account.")
        return redirect('home')
    else:
        # Handling the GET request for unauthenticated user

        # meta data
        title = 'Sign Up | CMS'
        params = {
            'title':title,
            'states':states
            }
        return render(request, 'general/signup.html', params)



def login_method(request):
    '''
        Handle the login reqest.\n
        It contain only POST request.\n
        GET request redirected to Home.
    '''
    # Handling the POST request
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            # login using email
            user = User.objects.get(email=username)
            user = authenticate(username = user.username, password = password)
        except:
            # login using username
            user = authenticate(username = username, password = password)

        if user == None:
            messages.error(request, 'Invalid Credentials. Try Again!')
            url = request.GET.get('next')
            return redirect(url)
        else:
            login(request, user)
            url = request.GET.get('next')
            messages.error(request, f'Hello {user.username}, Welcome Back!')
            return redirect(url)            
    else:
        # Hanling the GET request
        return redirect('home')


@login_required()
def logout_method(request):
    '''
        Handling the logout request.
    '''
    logout(request)
    messages.success(request, 'Successfully Logged Out.')
    try:
        url_next = request.GET.get('next')
        url = next_url(url_next)
        return redirect(url)
    except:
        return redirect('home')


@csrf_exempt
def available_email(request):
    '''
        Check the avalibility of email.\n
        Return True if email are available else True.
    '''
    email = request.POST.get('email').lower()
    avaibile_obj = User.objects.filter(email=email).exists()
    if avaibile_obj:
        return HttpResponse(False)
    else:
        if ' ' in email:
            # for handling spaces and non username words
            return HttpResponse(False)
        else:
            return HttpResponse(True)


@csrf_exempt
def available_username(request):
    '''
        Check the avalibility of username.\n
        Return True if username is available
    '''
    username = request.POST.get('username').lower()
    avaibile_obj = User.objects.filter(username=username).exists()
    if avaibile_obj:
        return HttpResponse(False)
    else:
        if ' ' in username or username in NON_USERNAME_WORDS:
            # for handling spaces and non username words
            return HttpResponse(False)
        else:
            return HttpResponse(True)


def forgot_password(request):
    '''
        Handle requests for forget password.\n
        Handle both POST and GET request.\n
        Redirect user to home if user is authenticated.\n
        This method do not reset the password, in POST request this method colled form data and send verification mail.\n
        Need to be Update.
    '''
    # Handle requests for if user is authenticated
    if request.user.is_authenticated:
        return redirect('home')
    # Handle request for unauthenticated user
    else:
        # handling POST request
        if request.method == 'POST':
            username = request.POST['fg-username'].lower()

            # getting user using email
            user = User.objects.filter(email=username).first()

            if user == None:
                # getting user using username
                user = User.objects.filter(username=username).first()
                
            if user == None:
                messages.error(request, 'Invalid data. Try Again!')

            # user_detail = User_detail.objects.get(user=user)
            # generating auth code
            otp = str(randint(100000, 999999));

            # saving user details
            # user_detail.otp = otp
            # user_detail.save()

            # generating activation url
            activation_url = FG_PASSWORD_URL_PREFIX + user.username + '/' + otp

            # Sending the activation email to new user
            html_content = render_to_string('general/fg-password-email.html', { 'user':user, 'url':activation_url})
            text_content = strip_tags(html_content)
            email_obj = EmailMultiAlternatives(FG_PASSWORD_MAIL_SUBJECT, text_content, settings.EMAIL_HOST_USER, to=[user.email])
            email_obj.attach_alternative(html_content, 'text/html')
            email_obj.send()
            messages.success(request, f'Please Check your Email {user.email}.')
            return redirect('home')
            
        # handling GET request
        else:
            return render(request, 'general/forgot-password.html')



@csrf_exempt
def update_password(request, username, otp):
    '''
        This method Reset password.\n
        Handle only POST request.\n
        POST request of reset password from email.\n
        Redirect to home in GET request  
    '''
    pass    


def districts(request):
    state = request.GET['state']
    districts_obj = AvailableDestination.objects.filter(state=state)
    districts = list()
    for obj in districts_obj:
        if obj.district in districts:
            continue
        districts.append(obj.district)
    params = {
        'district':districts,
        'status':True
    }
    return JsonResponse(params)


def pincodes(request):
    district = request.GET['district']
    pincode_obj = AvailableDestination.objects.filter(district=district)
    pincodes = list()
    cities = list()
    for obj in pincode_obj:
        if obj.pincode in pincodes:
            continue
        pincodes.append(obj.pincode)
        cities.append(obj.city)
    params = {
        'pincodes':pincodes,
        'cities':cities,
        'status':True
    }
    return JsonResponse(params)


# handling 404 error
def error_404(request, e):
    print('\n\nRunning')
    return render(request, '404.html')

# handling 404 error
def error_500(request):
    print('\n\nRunning')
    return render(request, '404.html')



        