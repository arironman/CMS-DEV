from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.html import mark_safe
from general.models import Faculty, states

# Create your models here.

def user_image_path(instance, filename):
    '''
        return the image path after renaming the image
    '''
    return f'images/user/{instance.user.id}/{filename}'





class CustomUser(AbstractUser):
    '''
        Extending the Build in User Model.
    '''
    gender = models.CharField(max_length=10, blank=True, verbose_name='Gender')
    mobile = models.CharField(verbose_name='Mobile Number', max_length=12, blank=True)
    dob = models.DateField(blank=True, null=True, verbose_name='Date Of Birth')
    image = models.ImageField(upload_to=user_image_path, default='user.png', verbose_name='User Image')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        suffix = self.groups.all().first()
        if suffix:
            return f'{self.username} - {suffix}'
        return f'{self.username}'

        
    @staticmethod
    def autocomplete_search_fields():
        return 'username'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def get_group_names(self):
        """
            get group, separate by comma, and display empty string if user has no group
        """

        return ','.join([group.name for group in self.groups.all()]) if self.groups.count() else ''

    # adding vebrose name to the method
    get_group_names.short_description = 'User Type'




class StaffUser(models.Model):
    '''
        Adding more require fields and stuff for our staff user
    '''
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE)
    faculty = models.ForeignKey("general.Faculty", verbose_name="Member of Faculty", on_delete=models.CASCADE, default=6)
    salary = models.FloatField(verbose_name='Salary', blank=True, null=True)
    date_join = models.DateField(blank=True, null=True)
    date_leave = models.DateField(blank=True, null=True)
    delivery_location = models.ForeignKey('general.AvailableDestination', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Delivery Location')

    class Meta:
        verbose_name = 'Staff User'
        verbose_name_plural = 'Staff Users'
        ordering = ['id']

    def __str__(self):
        return f'{self.user.username}'

    @staticmethod
    def autocomplete_search_fields():
        return 'user__username'


class UserAddress(models.Model):
    '''
        This address modal store the address of User  
    '''
    user = models.OneToOneField(CustomUser, verbose_name="User", on_delete=models.CASCADE, blank=True, null=True)
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
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'
        ordering = ['-id']

    def __str__(self):
        return f' {self.house_number},\n {self.street},\n {self.city},\n {self.state},\n {self.pincode}'
