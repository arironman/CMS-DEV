from django.db import models
from django.db.models.fields import CharField

# Create your models here.

states = [("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), ("Assam", "Assam"), ("Bihar", "Bihar"), ("Chhattisgarh", "Chhattisgarh"), ("Goa", "Goa"), ("Gujarat", "Gujarat"), ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"), ("Jammu and Kashmir", "Jammu and Kashmir"), ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"), ("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"), ("Maharashtra", "Maharashtra"), ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"), ("Nagaland", "Nagaland"), ("Odisha", "Odisha"), ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"), ("Sikkim", "Sikkim"), ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), ("Tripura", "Tripura"), ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), ("West Bengal", "West Bengal"), ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), ("Chandigarh", "Chandigarh"), ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), ("Daman and Diu", "Daman and Diu"), ("Lakshadweep", "Lakshadweep"), ("Delhi", "Delhi"), ("Puducherry", "Puducherry")]



class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=200, verbose_name='Street')
    city = models.CharField(max_length=50, verbose_name='City')
    district = models.CharField(max_length=50, verbose_name='District')
    state = models.CharField(max_length=50, blank=True, verbose_name='State', choices=states)
    pincode = models.CharField(max_length=6, verbose_name='Pincode')

    class Meta:
        verbose_name = 'Faculty Address'
        verbose_name_plural = 'Faculty Addresses'
        ordering = ['-id']

    def __str__(self):
        return f' {self.street},\n {self.city},\n {self.district},\n {self.state},\n {self.pincode}'


class AvailableDestination(models.Model):
    '''
        this modal store the valid destination(state, districts, city & pincode) where we can deliver.\n
        Its is connected to the Facuilty and User model to store the Linked faculty and delivery Boys
    '''
    city = models.CharField(verbose_name='City/Town', max_length=200)
    state = models.CharField(verbose_name='State', max_length=100, choices=states)
    district = models.CharField(verbose_name='District', max_length=100)
    pincode = models.CharField(max_length=10, verbose_name='Pincode')
    faculty = models.ForeignKey(Faculty, verbose_name='Faculty', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Available Destination'
        verbose_name_plural = 'Available Destinations'
        ordering = ['-id']

    def __str__(self):
        return f'{self.city}-{self.pincode}'

