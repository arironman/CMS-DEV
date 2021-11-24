from django.contrib.messages.api import error, success
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from general.views import pincodes

# models and other stuff
from user.models import CustomUser as User
from general.models import AvailableDestination, Faculty
from courier.models import Courier, CourierDeliveryStatus, DeliverAddress, PickupAddress, DeliverAddress
# from courier.forms import courier_form
from CMS.destination import state as states
from courier.utils import add_address, courier_date, get_courier_charge



# Create your views here.


@login_required()
def create_parcle(request):
    '''
        Handle the page create Parcle/Courier.\n
        Handle POST and GET request both.
    '''

    # handling the POST request
    if request.method == 'POST':
        # fetching form data
        recipient_name = request.POST['recipient-name']
        recipient_email = request.POST['recipient-email']
        title = request.POST['parcle-title']
        weight = request.POST['weight']
        parcle_desc = request.POST['desc']


        # creating and saving courier to database
        courier = Courier(customer=request.user, recipient_name=recipient_name,recipient_email=recipient_email, title=title, description=parcle_desc, weight=weight)
        courier.save()

        # creating and saving address to database
        deliver_obj = DeliverAddress(courier=courier)
        pickup_obj = PickupAddress(courier=courier)
        deliver_obj = add_address(deliver_obj, request, 'delivery')
        pickup_obj = add_address(pickup_obj, request, 'pickup')


        default_delivery_boy = User.objects.get(username='no-delivery-boy')

        pickup_faculty = AvailableDestination.objects.filter(pincode=pickup_obj.pincode).first().faculty
        deliver_faculty = AvailableDestination.objects.filter(pincode=deliver_obj.pincode).first().faculty

        # setting pickup and delivery date
        pickup_date, delivery_date = courier_date(pickup_faculty, deliver_faculty)
        courier.pickup_date = pickup_date


        # calculating charge
        charge = get_courier_charge(pickup_faculty, deliver_faculty, weight)
        courier.charge = charge
        courier.save()


        # creating record in courier delivery status
        status = CourierDeliveryStatus(courier=courier, delivery_boy=default_delivery_boy, pickup_faculty=pickup_faculty, deliver_faculty=deliver_faculty, delivered_date=delivery_date)
        status.save()

        

        messages.error(request, 'Courier Added Successfully')
        return redirect('courier_detail', courier_id=courier.id)
    # form = courier_form(request.POST or None, request.FILES or None)
    title = 'Create Parcle | CMS'

    params = {
        'title': title,
        # 'form': form
        'states':states
    }
    return render(request, 'courier/create-parcle.html', params)



@login_required()
def detail_parcle(request, courier_id):
    '''
        Handle the GET request of conform parcle.
    '''
    courier = Courier.objects.get(id=courier_id)
    if request.user.username != courier.customer.username:
        return redirect('home')

    pickup = PickupAddress.objects.get(courier=courier)
    deliver = DeliverAddress.objects.get(courier=courier)
    status = CourierDeliveryStatus.objects.get(courier=courier)
    params = {
        'courier':courier,
        'pickup':pickup,
        'deliver':deliver,
        'status':status

    }
    return render(request, 'courier/courier-detail.html', params)


@login_required()
def cancel_parcle(request, courier_id):
    '''
        Handle the GET request of cancle parcle.
    '''
    courier = Courier.objects.get(id=courier_id)
    if request.user.username != courier.customer.username:
        return redirect('home')
    courier.delete()

    messages.error(request, 'Courier cancel Successfully !')
    return redirect('home')



@login_required()
def conform_parcle(request, courier_id):
    '''
        Handle the GET request of conform parcle.
    '''
    courier = Courier.objects.get(id=courier_id)
    if request.user.username != courier.customer.username:
        return redirect('home')

    if courier.conform:
        return redirect('home')

    courier.conform = True
    courier.save()
    
    messages.error(request, 'Courier Placed Successfully.')
    return redirect('home')



@login_required()
def courier(request, courier_id):
    '''
        Handle the GET request of parcle.\n
        Shows the courier details and track record
    '''
    courier = Courier.objects.get(id=courier_id)

    if not courier.conform:
        return redirect('courier_detail', courier_id=courier_id)
    pickup = PickupAddress.objects.get(courier=courier)
    deliver = DeliverAddress.objects.get(courier=courier)
    status = CourierDeliveryStatus.objects.get(courier=courier)
    params = {
        'courier':courier,
        'pickup':pickup,
        'deliver':deliver,
        'status':status

    }
    return render(request, 'courier/courier.html', params)
