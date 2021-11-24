from general.forms import FacultyAdminForm
from user.models import CustomUser as User
from user.models import StaffUser
from django.contrib import admin
from general.models import AvailableDestination, Faculty
from jet.admin import CompactInline


# Register your models here.
class StaffUserInline(CompactInline):
    '''
        Creating inline for Staff User model.\n
        Used to add Staff User in Faculty model.
    '''
    model = StaffUser
    extra = 1
    show_change_link = True





class FacultyInline(CompactInline):
    '''
        Faculty inline model.\n
        Used to add in Faculty Modal in Custom User Modal.\n
        Only added in Faculty Members\n
    '''
    model = Faculty
    extra = 1
    show_change_link = True


class AvailableDestinationInline(CompactInline):
    '''
        Available Pincode inline model.\n
        Used to add in Available Pincode Modal in Faculty Modal.\n
    '''
    model = AvailableDestination
    extra = 1
    show_change_link = True




@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    '''
        Registering and stuff for Faculty Modal
    '''
    inlines = [AvailableDestinationInline, StaffUserInline]
    list_display = ['city', 'pincode', 'district', 'state']
    list_filter = ('city', 'state', 'pincode', 'district')
    search_fields = ('city__startswith', 'state__startswith',
                     'pincode__startswith', 'district__startswith')
    # form = FacultyAdminForm

    # setting permissions for groups
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Delivery Boy').exists():
            return False
        return True

    # setting permissions for groups
    def changeform_view(self, request, *args, **kwargs):
        self.readonly_fields = list(self.readonly_fields)
        if request.user.groups.filter(name='Employee').exists():
            self.readonly_fields = self.get_fields(request)

        return super().changeform_view(request, *args, **kwargs)




@admin.register(AvailableDestination)
class AvailableDestinationAdmin(admin.ModelAdmin):
    '''
        Registering and stuff for Available Destination Modal
    '''
    list_display = ['city', 'state', 'district', 'pincode']
    list_filter = ('state', 'district', 'pincode', 'faculty')
    search_fields = ('pincode__startswith', 'state__startswith', 'district__startswith')

    # setting permissions for groups
    def changeform_view(self, request, *args, **kwargs):
        self.readonly_fields = list(self.readonly_fields)
        if request.user.groups.filter(name='Employee').exists():
            self.readonly_fields = self.get_fields(request)
        return super().changeform_view(request, *args, **kwargs)
