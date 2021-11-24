from django.contrib import admin
from django.contrib.auth.models import Group
from user.models import CustomUser, UserAddress, StaffUser
from user.forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

from jet.admin import CompactInline
from jet.filters import DateRangeFilter

from jet.filters import RelatedFieldAjaxListFilter
from courier.models import Courier, CourierDeliveryStatus
from general.admin import FacultyInline 

class CourierDeliveryStatusDeliveryInline(CompactInline):
    '''
        Courier Delivery Status inline model.\n
        Used to add in Courier Delivery Status Modal in Custom User Modal.\n
        Show Data related to delivery_boy foreign key.
    '''
    model = CourierDeliveryStatus
    extra = 1
    show_change_link = True
    fk_name = 'delivery_boy'
    verbose_name = 'Courier for Delivery'
    verbose_name_plural = 'Couriers for Delivery'


class CourierDeliveryStatusShippingInline(CompactInline):
    '''
        Courier Delivery Status inline model.\n
        Used to add in Courier Delivery Status Modal in Custom User Modal.\n
        Show Data related to shipping_center foreign key.
    '''
    model = CourierDeliveryStatus
    extra = 1
    show_change_link = True
    fk_name = 'shipping_center'
    verbose_name = 'Shipped Courier'
    verbose_name_plural = 'Shipped Couriers'


class CourierInline(CompactInline):
    '''
        Courier inline model.\n
        Used to add in Courier Modal in Custom User Modal.
    '''
    model = Courier
    extra = 1
    show_change_link = True


class StaffUserInline(CompactInline):
    '''
        Staff User inline model.\n
        Used to add in User Modal, Courier status.
    '''
    model = StaffUser
    extra = 1
    show_change_link = True




class UserAddressInline(CompactInline):
    '''
        Creating inline for User Address model.\n
        Used to add User Address to Custom User model.
    '''
    model = UserAddress
    extra = 1
    show_change_link = True



class CustomUserInline(CompactInline):
    '''
        Creating inline for Custom User model.\n
        Used to add Custom User in User Address model.
    '''
    model = CustomUser
    extra = 1
    show_change_link = True




# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    '''
        This Class is to register the Custom User model but before registering we inherit the User Admin class (register class for Build in User model).
    '''
    model = CustomUser
    add_form = CustomUserCreationForm


    list_display = ("username", 'email', 'mobile',
                    'is_staff', 'get_group_names')
    list_filter = (*UserAdmin.list_filter, ('date_joined', DateRangeFilter))
    search_fields = (*UserAdmin.search_fields, 'mobile__startswith')



    fieldsets = [
        ('Authentication Details', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('image_tag', 'first_name', 'last_name', 'gender', 'dob')}),
        ('Contact info', {'fields': ('email', 'mobile')}),
        ('User Status and Type', {'fields': ('is_active', 'is_staff', 'is_superuser',), }),
        ('Group And Permissions', {'fields': ('groups', 'user_permissions'),}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    ]
    readonly_fields = ['image_tag']

    def get_inline_instances(self, request, obj=None):
        '''
            Setting inlines for different groups 
        '''
        self.inlines = [UserAddressInline, CourierInline]
        if obj:
            # below line is required
            # because next if condition throw error due to change on object data
            username = obj.username
            try:
                staff_status = CustomUser.objects.get(username=username).is_staff
                if staff_status:
                    self.inlines.append(StaffUserInline)

                if obj.groups.filter(name='Delivery Boy').exists():
                    self.inlines.append(CourierDeliveryStatusDeliveryInline)
                    # self.inlines.append(FacultyInline)

                elif obj.groups.filter(name='Faculty Employee').exists():
                    self.inlines.append(CourierDeliveryStatusShippingInline)
                    # self.inlines.append(FacultyInline)
            except:
                pass
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

        # setting permissions for groups

    # setting permissions for groups
    # def changeform_view(self, request, *args, **kwargs):
    #     self.readonly_fields = list(self.readonly_fields)
    #     if request.user.groups.filter(name='Delivery Boy').exists():
    #         read_only_field = ['username', 'password', 'image_tag', 'first_name', 'last_name', 'gender', 'dob', 'email', 'mobile', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined']
    #         self.readonly_fields += read_only_field

    #     return super().changeform_view(request, *args, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Delivery Boy').exists() or request.user.groups.filter(name='Faculty Employee').exists():
            return False
        return True


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    '''
        Registering and more stuff for User Address Modal
    '''
    list_display = ['user', 'house_number', 'city', 'pincode', 'district', 'state']
    list_filter = ('city', 'state', 'pincode', 'district')
    search_fields = ('city__startswith', 'state__startswith',
                     'pincode__startswith', 'district__startswith', 'user__username')




@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    '''
        Registering and more stuff for Staff User Modal
    '''
    # inlines = [CustomUserInline, FacultyInline]
    list_display = ['user', 'salary', 'date_join']
    list_filter = ('faculty__state', 'salary')
    # search_fields = ('state__startswith','pincode__startswith', 'district__startswith')
    search_fields = ('user__username__startswith',)

    fieldsets = [
        ('User Details', {
         'fields': ('user', 'salary', 'faculty', 'delivery_location')}),
        ('Important dates', {'fields': ('date_join', 'date_leave')}),
    ]

    def get_inline_instances(self, request, obj=None):
        '''
            Setting some options 
        '''
        self.readonly_fields = ['faculty', 'delivery_location']
        if obj:
            group = str(obj.user.groups.all().first())
            if group == 'Faculty Employee':
                self.readonly_fields.remove('faculty')
            if group == 'Delivery Boy':
                self.readonly_fields.remove('delivery_location')
        return super(StaffUserAdmin, self).get_inline_instances(request, obj)





# 
# def render_change_form(self, request, context, *args, **kwargs):
#    context['adminform'].form.fields['actors'].queryset = Actor.objects.filter(is_star=True)
#    return super().render_change_form(request, context, *args, **kwargs)
