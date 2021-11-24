from django import forms
from django.contrib.auth.models import Group
from courier import admin
from general.models import Faculty
from user.models import CustomUser as User

class FacultyAdminForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FacultyAdminForm, self).__init__(*args, **kwargs)
        # print('called')
        # group = Group.objects.get(name)
        # print(len(self.fields['faculty_employees'].queryset))
        self.fields['faculty_employees'].queryset = User.objects.filter(groups__name='Employee')
        # print(len(self.fields['faculty_employees'].queryset))