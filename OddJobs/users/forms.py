from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Employee, Employer

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    CHOICES = [('employer', 'Employer'), ('employee', 'Employee')]
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'location', 'contact_number']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
            user.UserRegisterForm = self  # Store a reference to the form in the User instance
            if user_type == 'employer':
                employer = Employer.objects.create(user=user)
            elif user_type == 'employee':
                employee = Employee.objects.create(user=user)
        return user




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    location = forms.CharField()
    contact_number = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'location', 'contact_number']


class ProfileUpdateForm(forms.ModelForm):
     class Meta:
          model = Profile
          fields = ['image']



