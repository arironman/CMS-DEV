from django.contrib import admin
from django.http import request

from courier.models import Courier, CourierDeliveryStatus, DeliverAddress, PickupAddress
from jet.admin import CompactInline

from jet.filters import RelatedFieldAjaxListFilter
from jet.filters import DateRangeFilter
from user.models import CustomUser


# Register your models here.
class CourierDeliveryStatusInline(CompactInline):
    '''
        Courier Delivery Status inline model.\n
        Used to add in Courier Delivery status in Courier Modal.
    '''
    model = CourierDeliveryStatus
    extra = 1
    show_change_link = True

class PickUpAddressInline(CompactInline):
    '''
        Pick Up Address inline model.\n
        Used to add in Pick Up Address in Courier Modal.\n
        Connected to Foreign Key courier
    '''
    model = PickupAddress
    extra = 1
    show_change_link = True
    fk_name = 'courier'
    verbose_name = "Pick Up Address"
    verbose_name_plural = "Pick Up Addresses"


class DeliverAddressInline(CompactInline):
    '''
        Deliver Address inline model.\n
        Used to add in Deliver Address in Courier Modal.\n
        Connected to Foreign Key courier
    '''
    model = DeliverAddress
    extra = 1
    show_change_link = True
    fk_name = 'courier'
    verbose_name = "Deliver Address"
    verbose_name_plural = "Deliver Addresses"


@admin.register(PickupAddress)
class PickUpAddressAdmin(admin.ModelAdmin):
    '''
        Registering and stuff for Pick Up Address Modal
    '''
    list_display = ['courier', 'city', 'pincode', 'district', 'state']
    list_filter = ('city', 'state', 'pincode', 'district')
    search_fields = ('city__startswith', 'state__startswith',
                     'pincode__startswith', 'district__startswith')


@admin.register(DeliverAddress)
class DeliverAddressAdmin(admin.ModelAdmin):
    '''
        Registering and stuff for Deliver Address Modal
    '''
    list_display = ['courier', 'city', 'pincode', 'district', 'state']
    list_filter = ('city', 'state', 'pincode', 'district')
    search_fields = ('city__startswith', 'state__startswith',
                     'pincode__startswith', 'district__startswith')




@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    inlines = [PickUpAddressInline, DeliverAddressInline,
               CourierDeliveryStatusInline]
    list_display = ('title', 'id', 'customer', 'weight', 'charge', 'pickup_date')
    search_fields = ('recipient_name__startswith', 'customer__username__startswith')

    list_filter = [('customer', RelatedFieldAjaxListFilter),
                   'rating', ('register_date', DateRangeFilter),
                   'conform']

    fieldsets = (
        ('Recipient and User Details', {
         'fields': ('customer', 'recipient_name', 'recipient_email')}),
        ('Courier Details', {
         'fields': ('title', 'description', 'weight', 'charge', 'conform')}),
        ('Important Dates', {'fields':('register_date', 'pickup_date')}),
        ('Ratings and Feedback', {'fields':('rating', 'feedback')})
    )

    readonly_fields = ['register_date',]

    
    # setting permissions for groups
    def changeform_view(self, request, *args, **kwargs):
        self.readonly_fields = list(self.readonly_fields)
        if request.user.groups.filter(name='Delivery Boy').exists():
            read_only_field = ['customer',
                               'recipient_name', 'recipient_email', 'title', 'description', 'weight', 'charge', 'register_date', 'pickup_date', 'rating', 'feedback']
            self.readonly_fields += read_only_field

        return super().changeform_view(request, *args, **kwargs)


@admin.register(CourierDeliveryStatus)
class CourierDeliveryStatusAdmin(admin.ModelAdmin):
    '''
        Register the Courier Delivery Status Model\n
    '''    
    list_display = ('courier', 'pickup_faculty',
                    'deliver_faculty', 'delivery_boy', 'is_shipped', 'is_delivered')

    search_fields = ('courier__recipient_name__startswith', 'customer__username__startswith',)

    list_filter = [('delivery_boy', RelatedFieldAjaxListFilter), ('pickup_faculty', RelatedFieldAjaxListFilter), ('deliver_faculty', RelatedFieldAjaxListFilter), 'is_picked','is_shipped', 'is_delivered', 'out_for_delivery']
    fieldsets = (
        ('Courier Details', {
         'fields': ('courier', 'pickup_faculty', 'deliver_faculty', 'delivery_boy', 'delivered_date')}),
        ('Courier Status', {
         'fields': ('is_picked', 'is_shipped', 'out_for_delivery', 'is_delivered')}),
        )


    def changeform_view(self, request, *args, **kwargs):
        '''
            setting read only permissions for diffrent groups
        '''
        self.readonly_fields = list(self.readonly_fields)
        if request.user.groups.filter(name='Delivery Boy').exists():
            read_only_fields = ['is_shipped', 'out_for_delivery', 'delivery_boy']
            self.readonly_fields += read_only_fields
        elif request.user.groups.filter(name='Faculty Employee').exists():
            read_only_fields = ['is_delivered']
            self.readonly_fields += read_only_fields
        elif request.user.groups.filter(name='Employee').exists():
            read_only_fields = ['is_picked', 'delivery_boy',
                                'is_shipped', 'out_for_delivery', 'is_delivered']
            self.readonly_fields += read_only_fields
        

        return super().changeform_view(request, *args, **kwargs)

