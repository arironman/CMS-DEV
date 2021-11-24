from django.contrib.messages.api import error, success
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from CMS.variables import *
from user.utils import get_input_field, check_valid_email, check_valid_username, send_otp, verification_email

# models and other stuff
from user.models import CustomUser as User
from user.models import UserAddress
from general.models import AvailableDestination 
from CMS.destination import state as states


@login_required()
def name(request):
    '''
        GET request -> return the name of user\n
        POST request -> Update the name of user 
    '''
    # Handling the POST Request
    if request.method == 'POST':

        name = request.POST['data']

        # validating name
        if name != ' ' and len(name) > 3:
            name_list = name.split(' ')
            if len(name_list) > 1:
                last_name = name_list[-1]
                name_list.pop()
                first_name = ' '.join(name_list)
            else:
                first_name = name_list[0]
                last_name = ''

            # updating the data into database
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()

            status = True
            message = 'Name Updated Successfully!'
        else:
            status = False
            message = 'Invalid Name. Try Again!'

        messages.error(request, message)
        params = {
            status: status,
            'data': name
        }

        return redirect('user')
        # return render(request, 'user/profile.html')
    # Handling the GET Request
    # fetching the json data in ajax request
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    name = request.user.first_name + ' ' + request.user.last_name
    input_field = f'''
        <div class="form-group">
            <input type="text" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data" onkeypress="return (event.charCode > 64 && event.charCode < 91) || (event.charCode > 96 && event.charCode < 123) || (event.charCode==32)">
        </div>'''
    params = {
        'data': name,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def username(request):
    '''
        GET request -> return the username of user\n
        POST request -> Update the username of user 
    '''

    # handling the POST Request
    if request.method == 'POST':
        username = request.POST['data']
        if check_valid_username(username):
            # updating the data in database
            request.user.username = username
            request.user.save()
            status = True
            message = 'Username Updated Successfully!'
        else:
            status = False
            message = 'Invalid Username. Try Again!'

        messages.error(request, message)
        params = {
            status: status,
            username: username
        }
        return redirect('user')

    # handling the GET Request
    # fetching the json data in ajax request
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    input_field = f'''
        <div class="form-group valid">
            <input type="text" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data" onkeyup="usernameStatus('new-username')">
            <span class="fas" id="username-checker"></span>
        </div>'''
    params = {
        'data': request.user.username,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def gender(request):
    '''
        GET request -> Return the gender of user\n
        POST request -> Update the gender of user
    '''
    # handling the POST Request
    if request.method == 'POST':
        gender_list = ['male', 'female', 'other']

        gender = request.POST['data'].lower()
        if gender in gender_list:
            # updating the database
            request.user.gender = gender
            request.user.save()

            status = True
            message = 'Gender Updated Successfully!'

        else:
            status = False
            message = 'Invalid Value!'

        params = {
            'status': status,
            'gender': gender
        }
        messages.error(request, message)
        return redirect('user')

    # handling the GET Request
    # fetching the json data in ajax request
    field = request.POST.get('field')
    url_keyword = request.POST.get('urlKeyword')

    gender = request.user.gender
    input_field = f'''
        <div class="form-group">
            <select name="data" class='form-control' id="new-{url_keyword}" placeholder='New {field}'>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
            </select>
        </div>'''

    params = {
        'data': gender,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def email(request):
    '''
        GET request -> Return the email of user\n
        POST request -> Update the email of user 
    '''
    # handling the POST Request
    if request.method == 'POST':
        email = request.POST['data'].lower()
        if check_valid_email(email):
            # validation & stuff
            send_otp(email)
            verification_email(email)

            # updating the data
            request.user.email = email
            request.user.save()

            status = True
            message = 'Email Updated Successfully!'
        else:
            status = False
            message = 'Inavalid Email. Try Another!'

        params = {
            'status': status,
            'data': email
        }
        messages.error(request, message)
        return redirect('user')

    # handling the GET Request
    # fetching the json data in ajax request
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    input_field = f'''
        <div class="form-group valid">
            <input type="email" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data" onkeyup="emailStatus('new-email')">
            <span class="fas" id="email-checker"></span>
        </div>'''

    params = {
        'data': request.user.email,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def mobile(request):
    '''
        GET request -> Return the mobile number of user\n
        POST request -> Update the mobile number of user 
    '''
    # Handling the POST Request
    if request.method == 'POST':
        mobile = request.POST['data']
        if mobile.isnumeric():
            # updating the database
            request.user.mobile = mobile
            request.user.save()

            status = True
            message = 'Mobile Number is Updated Successfully!'
        else:
            status = False
            message = 'Invalid Mobile Number. Try Again'

        params = {
            'data': mobile,
            'status': status
        }
        messages.error(request, message)
        return redirect('user')

    # Handling the GET Request
    # fetching ajax data
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    mobile = request.user.mobile
    input_field = f'''
        <div class="form-group">
            <input type="tel" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data" onkeypress='return event.charCode >= 48 && event.charCode <= 57' minlength=10 maxlength=12>
        </div>'''

    params = {
        'data': mobile,
        'input': input_field
    }
    return JsonResponse(params)


# for addresses

@login_required()
def house_number(request):
    '''
        GET request -> Return the house number of user\n
        POST request -> Update the house number of user 
    '''
    # handle the POST Request
    if request.method == 'POST':
        house_number = request.POST['data']

        # fetching and updating the data
        address = UserAddress.objects.get(user=request.user)
        address.house_number = house_number
        address.save()

        messages.error(request, 'Address is Updated Successfully!')
        params = {
            'data': house_number,
            'status': True
        }
        return redirect('user')

    # handle the GET Request
    # fetching ajax data
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    input_field = f'''
        <div class="form-group">
            <input type="text" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data">
        </div>'''
    address = UserAddress.objects.get(user=request.user)

    params = {
        'data': address.house_number,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def street(request):
    '''
        GET request -> Return the street of user\n
        POST request -> Update the street of user
    '''

    # handling the POST Request of user
    if request.method == 'POST':
        street = request.POST['data']

        # fetching and updating the data
        address = UserAddress.objects.get(user=request.user)
        address.street = street
        address.save()
        messages.error(request, 'Address is Updated Successfully!')

        params = {
            'data': street,
            'status': True
        }
        return redirect('user')

    # handling the GET Request of user
    # fetching ajax data
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    input_field = f'''
        <div class="form-group">
            <input type="text" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data">
        </div>'''
    address = UserAddress.objects.get(user=request.user)

    params = {
        'data': address.street,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def city(request):
    '''
        GET request -> return the city of user
        POST request -> Update the city of user 
    '''
    # Handling the GET Request
    if request.method == 'POST':
        city = request.POST['data']

        # fetching and modifying the data
        address = UserAddress.objects.get(user=request.user)
        address.city = city
        address.save()

        messages.error(request, 'Address is Updated Successfully!')

        params = {
            'data': city,
            'status': True
        }
        return redirect('user')

    # Handling the POST Request
    # fetching ajax data
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    input_field = f'''
        <div class="form-group">
            <input type="text" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data">
        </div>'''
    address = UserAddress.objects.get(user=request.user)

    params = {
        'data': address.city,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def district(request):
    '''
        GET request -> return the district of user
        POST request -> Update the district of user 
    '''
    # Handling the POST Request
    if request.method == 'POST':
        district = request.POST['data']

        # fetching and updating the data
        address = UserAddress.objects.get(user=request.user)
        address.district = district
        address.save()

        messages.error(request, 'Address is Updated Successfully!')
        params = {
            'data': district,
            'status': True
        }
        return redirect('user')

    # Handling the GET Request
    # fetching ajax data
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    address = UserAddress.objects.get(user=request.user)

    # making a list of available districts
    districts_obj = AvailableDestination.objects.filter(state=address.state)
    districts = list()
    district_html = ''
    for obj in districts_obj:
        if obj.district in districts:
            continue
        districts.append(obj.district)
        district_html += f'<option value="{obj.district}">{obj.district}</option>'

    input_field = f'''
        <div class="form-group">
            <select name="data" class="form-control" aria-placeholder="District" id='new-{url_keyword}'>
            {district_html}
            </select>
        </div>'''

    params = {
        'data': address.district,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def state(request):
    '''
        GET request -> Return the state of user\n
        POST request -> Update the state of user
    '''
    # Handling the POST Request
    if request.method == 'POST':
        state = request.POST['data']

        # fetching and updating the data
        address = UserAddress.objects.get(user=request.user)
        address.state = state
        address.save()

        messages.error(request, 'Address is Updated Successfully!')

        params = {
            'data': state,
            'status': True
        }
        return redirect('user')

    # Handling the GET Request
    # fetching ajax data
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    # add options of all state for html
    options = ''
    for state in states:
        options += f'<option value="{state}">{state}</option >'

    input_field = f'''
        <div class="form-group">
            <select name="data" class='form-control' id="new-{url_keyword}" placeholder='New {field}'>
                {options}
            </select>
        </div>'''
    address = UserAddress.objects.get(user=request.user)

    params = {
        'data': address.state,
        'input': input_field
    }
    return JsonResponse(params)


@login_required()
def pincode(request):
    '''
        GET request -> Return the pincode of user\n
        POST request -> Update the pincode of user.
    '''
    # handling the POST Request
    if request.method == 'POST':
        pincode = request.POST['data']

        # fetching and updating the data
        address = UserAddress.objects.get(user=request.user)
        address.pincode = pincode
        address.save()

        messages.error(request, 'Address is Updated Successfully!')
        params = {
            'data': pincode,
            'status': True
        }
        return redirect('user')

    # handling the GET Request
    # fetching ajax data
    field = request.GET.get('field')
    url_keyword = request.GET.get('urlKeyword')

    address = UserAddress.objects.get(user=request.user)

    # making a list of available districts
    pincodes_obj = AvailableDestination.objects.filter(district=address.district)
    pincodes = list()
    pincode_html = ''
    for obj in pincodes_obj:
        if obj.pincode in pincodes:
            continue
        pincodes.append(obj.pincode)
        pincode_html += f'<option value="{obj.pincode}">{obj.pincode}</option>'

    input_field = f'''
        <div class="form-group">
            <select name="data" class="form-control" aria-placeholder="Pincode" id='new-{url_keyword}'>
            {pincode_html}
            </select>
        </div>'''

    params = {
        'data': address.pincode,
        'input': input_field
    }
    return JsonResponse(params)
