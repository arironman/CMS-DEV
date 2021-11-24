from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courier.models import Courier, CourierDeliveryStatus
from courier.views import courier
from user.models import UserAddress


# Create your views here.
# user profile
@login_required()
def user(request):
    '''
        Handle the user profile.\n
        Contain Only GET request.\n
        Contain Login Required Decorator.\n
        Need to Modify.

    '''
    address = UserAddress.objects.get(user=request.user)
    status = CourierDeliveryStatus.objects.filter(
        courier__customer=request.user)

    params = {
        'title': f'{request.user.username} Profile | CMS',
        # 'couriers':couriers,
        'address':address,
        'status':status
        }
    return render(request, 'user/profile.html', params)
