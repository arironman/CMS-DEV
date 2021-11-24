# we'll create it for some admin stuff

from django.contrib.auth.models import Group
from django.http.response import HttpResponse, JsonResponse
from general.models import AvailableDestination, Faculty
from user.models import CustomUser as User
from user.models import UserAddress, StaffUser
from datetime import date
import random

def get_details(path="static/admin/destination.txt"):
    '''
        Fetch the data and return the iterable data
        details -> list of many city detail
        details[index] -> list of single city detail 
        details[index][0] -> city name
        details[index][1] -> pincode
        details[index][2] -> state
        details[index][3] -> district
    '''
    details = list()
    with open(path, "r") as f:
        data = f.read()
        lines = data.split('\n')
        for line in lines:
            details.append(line.split('\t'))
    return details


def adding_user_address(user, city, pincode, district, state):
    '''
        Method used to add address in User Address Modal and return the address object.
    '''
    house_number = f'{user.username} House Number'
    street = f'{user.username} street'
    address = UserAddress(user=user, house_number=house_number, street=street, city=city, pincode=pincode, district=district, state=state)
    address.save()
    return address


def get_random_phone():
    '''
        return random phone number
    '''
    ph_no = []
  
    ph_no.append(random.randint(6, 9))
  
    for i in range(1, 10):
        ph_no.append(random.randint(0, 9))
    phone = ''.join([str(elem) for elem in ph_no])
    return phone

# def check_username(username):
#     '''
#         check and return unused username
#     '''
#     if User.objects.filter(username=username).exists():
#         username = username+'-'
#         for i in range(0,3):
#             username = username+str(random.randint(1, 9))
#     return username


def add_destination(request, faculty_pincode):
    '''
        This function is used to add the destinations from a text file present in static/admin/destination.txt\n
        we'll convert in list and add in available destination modal
    '''
    # url from where we copied the dstination stuff
    # link = https://www.mapsofindia.com/pincode/india/gujarat/ahmedabad/

    faculty = Faculty.objects.get(pincode=faculty_pincode)
    delivery_list = ['delivery-1', 'delivery-2']
    group = Group.objects.get(name='Delivery Boy')
    details = get_details()
    for detail in details:
        city = detail[0]
        pincode = detail[1]
        state = detail[2]
        district = detail[3]
    

        # skipping the cities having spaces
        if len(detail)>4:
            continue

        # add city to available address
        if AvailableDestination.objects.filter(pincode=pincode).exists():
            continue
        destination = AvailableDestination(city=city, pincode=pincode, district=district, state=state, faculty=faculty)
        destination.save()

        for delivery_boy in delivery_list:
            
            # creating user
            email = f'{delivery_boy}_{pincode}@cms.com'
            username = f'{delivery_boy}_{pincode}'
            user = User(username=username, email=email, password='anurag333')
            user.first_name = delivery_boy
            user.last_name = ''
            user.is_active = True
            user.is_staff = True
            user.gender = 'male'
            user.mobile = get_random_phone()
            user.save()
            print(user.username)

            # adding user to faculty employee group
            group.user_set.add(user)
            group.save()

            # creating address
            address = adding_user_address(user, city, pincode, district, state)

            # creating staff status
            staff = StaffUser(user=user, salary=10000, date_join=date.today(), delivery_location=destination)
            staff.save()
    return HttpResponse('Success') 

     
def add_faculty_members(request, faculty_pincode):
    faculty = Faculty.objects.get(pincode=faculty_pincode)
    faculty_list = ['faculty-1', 'faculty-2', 'faculty-3', 'faculty-4', 'faculty-5']
    group = Group.objects.get(name='Faculty Employee')
    for faculty_member in faculty_list:
        
        # creating user
        email = f'{faculty_member}_{faculty.pincode}@cms.com'
        username = f'{faculty_member}-{faculty.pincode}'
        user = User(username=username, email=email, password='anurag333')
        user.first_name = faculty_member
        user.last_name = ''
        user.is_active = True
        user.is_staff = True
        user.gender = 'male'
        user.mobile = get_random_phone()
        user.save()
        print(user.username)
        
        # adding user to faculty employee group
        group.user_set.add(user)
        group.save()

        # creating address
        address = adding_user_address(user, faculty.city, faculty.pincode, faculty.district, faculty.state)

        # creating staff status
        staff = StaffUser(user=user, salary=15000, date_join=date.today(), faculty=faculty)
        staff.save()
    
    return HttpResponse('success')

def test(request):
    # users = User.objects.filter(groups__name='Employee')
    # params = dict()
    # for user in users:
    #     params[user.username] = user.email        

  
    ph_no = []
  
    ph_no.append(random.randint(6, 9))
  
    for i in range(1, 10):
        ph_no.append(random.randint(0, 9))
    phone = ''.join([str(elem) for elem in ph_no])
    params = {
        'Phone': phone
    }
    return JsonResponse(params)