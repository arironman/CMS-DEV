from django.db import models
from user.models import CustomUser
from general.models import Faculty, states


# Create your models here.


class Courier(models.Model):
    '''
        This modal store the courier details
    '''
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name='Parcle Title')
    description = models.TextField(blank=True, default='NO DESCRIPTION', null=True, verbose_name='Parcle Description')
    weight = models.FloatField(verbose_name='Parcle Weight')
    charge = models.FloatField(verbose_name='Charge', blank=True, null=True)
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Customer User')    
    recipient_name = models.CharField(max_length=100, verbose_name='Recipient Name')
    recipient_email = models.CharField(max_length=200, verbose_name='Recipient Email')
    register_date = models.DateField(
        auto_now_add=True, verbose_name='Parcle Register Date')
    pickup_date = models.DateField(
        blank=True, null=True, verbose_name='Pick Up Date')
    rating = models.FloatField(
        blank=True, null=True, verbose_name='Delivery Rating')
    feedback = models.TextField(
        blank=True, default='NO FEEDBACK', null=True, verbose_name='Delivery Feedback')
    conform = models.BooleanField(default=False)


    class Meta:
        ordering = ['-id']
        verbose_name = 'Courier'
        verbose_name_plural = 'Couriers'

    def __str__(self):
        return f'{self.title} - {self.customer.username}'

    @staticmethod
    def autocomplete_search_fields():
        return 'customer__username', 'pickup_address__state', 'deliver_address__state'





class CourierDeliveryStatus(models.Model):
    '''
        This model is accessible to delivery boy and Faculty, which is mainly design to update the delivery status.
    '''
    id = models.AutoField(primary_key=True)
    courier = models.OneToOneField(Courier, related_name='courier', on_delete=models.CASCADE, verbose_name='Courier')
    delivery_boy = models.ForeignKey(CustomUser, related_name='delivary_boy', blank=True, null=True, verbose_name='Delivery Boy', limit_choices_to={'groups__name': "Delivery Boy"}, on_delete=models.SET_NULL)
    pickup_faculty = models.ForeignKey(Faculty, blank=True, verbose_name='Pick Up Faculty', related_name='pick_up_faculty', on_delete=models.DO_NOTHING, null=True)
    deliver_faculty = models.ForeignKey(Faculty, blank=True, verbose_name='Deliver Faculty',
                                        on_delete=models.DO_NOTHING, null=True, related_name='deliver_faculty')
    is_shipped = models.BooleanField(verbose_name='Courier is Shipped', default=False)
    out_for_delivery = models.BooleanField(verbose_name='Courier is Out for Delivery', default=False)
    is_delivered = models.BooleanField(verbose_name='Courier Delivered', default=False)
    is_picked = models.BooleanField(verbose_name='Courier Picked Up', default=False)
    delivered_date = models.DateField(blank=True, null=True, verbose_name='Delivered Date')
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Courier Status'
        verbose_name_plural = 'Couriers Status'

    def __str__(self):
        return f'{self.courier.title} - {self.delivery_boy.username}'

    @staticmethod
    def autocomplete_search_fields():
        return 'delivary_boy__username', 'shipping_center__username'



class PickupAddress(models.Model):
    '''
        This modal store the pickup address of particular courier.
    '''
    courier = models.ForeignKey(Courier, verbose_name='Courier Details', on_delete=models.CASCADE)
    house_number = models.CharField(
        max_length=200, blank=True, verbose_name='House Number')
    street = models.CharField(
        max_length=200, blank=True, verbose_name='Street')
    city = models.CharField(max_length=50, blank=True, verbose_name='City')
    district = models.CharField(
        max_length=50, blank=True, verbose_name='District')
    state = models.CharField(max_length=50, blank=True,
                             verbose_name='State', choices=states)
    pincode = models.CharField(
        max_length=10, blank=True, verbose_name='Pincode')

    class Meta:
        verbose_name = 'Pick Up Address'
        verbose_name_plural = 'Pick Up Addresses'
        ordering = ['-id']

    def __str__(self):
        return f' {self.house_number},\n {self.street},\n {self.city},\n {self.district},\n {self.state},\n {self.pincode}'



class DeliverAddress(models.Model):
    '''
        This modal store the Deliver address of particular courier.
    '''
    courier = models.ForeignKey(Courier, verbose_name='Courier Details', on_delete=models.CASCADE)
    house_number = models.CharField(
        max_length=200, blank=True, verbose_name='House Number')
    street = models.CharField(
        max_length=200, blank=True, verbose_name='Street')
    city = models.CharField(max_length=50, blank=True, verbose_name='City')
    district = models.CharField(
        max_length=50, blank=True, verbose_name='District')
    state = models.CharField(max_length=50, blank=True,
                             verbose_name='State', choices=states)
    pincode = models.CharField(
        max_length=10, blank=True, verbose_name='Pincode')

    class Meta:
        verbose_name = 'Deliver Address'
        verbose_name_plural = 'Deliver Addresses'
        ordering = ['-id']

    def __str__(self):
        return f' {self.house_number},\n {self.street},\n {self.city},\n {self.district},\n {self.state},\n {self.pincode}'







# class CourierAddress(models.Model):
#     '''
#         This modal store the pickup and delivary address of particular courier.
#     '''
#     courier = models.ForeignKey(Courier, verbose_name='Courier Details', on_delete=models.CASCADE)
#     house_number = models.CharField(
#         max_length=200, blank=True, verbose_name='House Number')
#     street = models.CharField(
#         max_length=200, blank=True, verbose_name='Street')
#     city = models.CharField(max_length=50, blank=True, verbose_name='City')
#     district = models.CharField(
#         max_length=50, blank=True, verbose_name='District')
#     state = models.CharField(max_length=50, blank=True,
#                              verbose_name='State', choices=states)
#     pincode = models.CharField(
#         max_length=10, blank=True, verbose_name='Pincode')

#     class Meta:
#         verbose_name = 'Courier Address'
#         verbose_name_plural = 'Courier Addresses'
#         ordering = ['-id']

#     def __str__(self):
#         return f' {self.house_number},\n {self.street},\n {self.city},\n {self.district},\n {self.state},\n {self.pincode}'


