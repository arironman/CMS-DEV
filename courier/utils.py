from datetime import datetime, timedelta
import calendar

def get_courier_charge(pickup, deliver, weight):
    '''
        method return the calculated charge
    '''
    weight = int(weight)
    # normal charge
    charge = weight*10

    # adding charge upon weight
    if weight >= 1000:
        additional_charge = weight*5 
        charge += additional_charge
    elif weight >= 800:
        additional_charge = weight*4 
        charge += additional_charge
    elif weight >= 500:
        additional_charge = weight*3 
        charge += additional_charge
    elif weight >= 300:
        additional_charge = weight*2 
        charge += additional_charge
    elif weight >= 100:
        additional_charge = weight*1 
        charge += additional_charge

    # charger upon distance(add only if states are not same)
    if pickup.state != deliver.state:
        charge += 200

    return charge


def courier_date(pickup, deliver):
    '''
        return the pick date & deliver date
    '''
    # calculating pickup date
    time = datetime.now()
    if time.hour >= 8:
        pickup_date = time + timedelta(days=1)             
    else:
        pickup_date = time

    # calculating deliver date
    if pickup.state != deliver.state:
        deliver_date = pickup_date + timedelta(days=5)
    else:
        deliver_date = pickup_date + timedelta(days=3)

    return pickup_date.date(), deliver_date.date()



def add_address(address_obj, request, prefix):
    '''
        Fetch pick up and delivery address and save into Courier_address Modal.\n
        Return the address model object.
    '''
    # fetching the address details
    address_obj.house_number = request.POST[f'{prefix}-house-no']
    address_obj.street = request.POST[f'{prefix}-street']
    address_obj.city = request.POST[f'{prefix}-city']
    address_obj.state = request.POST[f'{prefix}-state']
    address_obj.district = request.POST[f'{prefix}-district']
    address_obj.pincode = request.POST[f'{prefix}-pincode']

    # save address to database
    address_obj.save()
    return address_obj
