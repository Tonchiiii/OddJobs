from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import DetailView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from jobs.forms import JobListingForm
from jobs.models import JobListing
from portal.models import Post
from .models import Profile, Employee
import requests

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            location = form.cleaned_data.get('location')
            username = form.cleaned_data.get('username')
            location = form.cleaned_data.get('location')
            contact_number = form.cleaned_data.get('contact_number')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account Created for {username}! You can now log in.')
            profile = user.profile
            profile.first_name = first_name
            profile.last_name = last_name
            profile.location = location
            profile.contact_number = contact_number
            profile.email = email
            profile.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render (request, 'users/register.html', {'form':form})

    


@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.author = request.user
            job_listing.save()
            return redirect(reverse('portal-job_single', args=[job_listing.pk])
)
    else:
        form = JobListingForm()
        
    return render(request, 'users/post_job.html', {'form': form})

    

'''
def job_listings(request):
    job_listings = JobListing.objects.all()
    context = {'job_listings':job_listings}
    return render(request, 'portal/job_listings.html', context)
'''

'''
@login_required
def profile(request):
    return render(request, 'users/profile.html')
'''

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been updated.')
            return redirect('profile')
        else:
            # Render an error page or redirect to a different view for unauthorized access
            pass

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    
    return render(request, 'users/profile.html', context)


class Employee_ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/employee_profile.html'
    context_object_name = 'prof'
    login_url = '/login/'


def employee_profile(request, pk):
    if pk:
        prof = Profile.objects.filter(pk=pk).first()
    args = {'prof':prof}
    return render(reverse(request, 'users/employee_profile.html', args))


#GCASH PAYMENT THRU PAYMONGO
def payment_page(request):
    return render(request, 'users/payment_page.html')


def payment_post(request):
    url = "https://api4wrd-v1.kpa.ph/paymongo/v1/create"
    app_key = "2983411fd6504ce5707e915b96fec0aa00125103"
    secret_key = "sk_test_DRXZ3p8DvSj9Mgu9PMhCvGvA"
    password = "your-paymongo-password"

    # get the necessary data from the request
    email = request.GET.get('email')
    first_name = request.GET.get('firstName')
    last_name = request.GET.get('lastName')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    address2 = request.GET.get('address2')
    city = request.GET.get('city')
    state = request.GET.get('state')
    zip_code = request.GET.get('zip')
    country = request.GET.get('country')

    redirect_urls = {
        "success": "payment_success",
        "failed": "users/payment_failed"
    }

    billing = {
        "email": email,
        "name": f"{first_name} {last_name}",
        "phone": mobile,
        "address": {
            "line1": address,
            "line2": address2,
            "city": city,
            "state": state,
            "postal_code": zip_code,
            "country": country
        }
    }

    attributes = {
        "livemode": False,
        "type": "gcash",
        "amount": 10000,
        "currency": "PHP",
        "redirect": redirect_urls,
        "billing": billing,
    }

    source = {
        "app_key": app_key,
        "secret_key": secret_key,
        "password": password,
        "data": {
            "attributes": attributes
        }
    }

    response = requests.post(url, json=source, verify=False)

    if response.status_code == 200:
        response_data = response.json()
        return redirect(response_data["url_redirect"])
    else:
        return render(request, 'payment_failed.html')


def payment_success(request):
    if 'ukayra_id' in request.GET:
        ukayra_id = request.GET['ukayra_id']
        paymongo_id = request.GET.get('paymongo_id', None)
        method = request.GET.get('method', None)
        message = request.GET.get('message', None)
        context = {
            'ukayra_id': ukayra_id,
            'paymongo_id': paymongo_id,
            'method': method,
            'message': message
        }
        return redirect(request, 'users/payment_success.html', context)
    else:
        return redirect(request, 'users/payment_success.html')
    
def payment_failed(request):
    if 'ukayra_id' in request.GET:
        response = "UkayraID: " + request.GET['ukayra_id'] + "<br />"

        if 'method' in request.GET:
            response += "Method: " + request.GET['method'] + "<br />"

        if 'message' in request.GET:
            response += "Error Message: " + request.GET['message']
    else:
        response = "Failed Page"

    response += '<br><a href="/demo">Back to main</a>'

    return HttpResponse(response)
    
