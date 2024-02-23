from django import forms
from .models import JobListing, Job
from portal.models import Post

class JobListingForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    requirements = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ('title', 'description', 'requirements', 'location', 'salary')



class JobPostingForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    requirements = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=100)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)
    start_date = forms.DateField()
    end_date = forms.DateField()

    class Meta:
        model = JobListing
        fields = ['title', 'description', 'requirements', 'location', 'salary', 'start_date', 'end_date']

    def save(self, employer, commit=True):
        instance = super(JobListingForm, self).save(commit=False)
        instance.author = employer.name # Set the author field to the name of the employer
        if commit:
            instance.save()
        return instance