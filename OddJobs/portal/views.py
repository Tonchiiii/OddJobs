from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Post
from users.models import Profile, Employee
from jobs.forms import JobPostingForm, JobListingForm
from jobs.models import Employer_Notification, Employee_Notification, JobListing

def home(request, pk):
    if pk:
        confirm = Post.objects.filter(pk=pk)
    args = {'confirm':confirm}
	
    context = {
		'posts': Post.objects.all()
	}
    return render(request, 'portal/home.html', context, args)

class PostListView(ListView):
    model = Post
    template_name = 'portal/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    
class ConfirmationDetailView(DetailView):
    model = Post
    template_name = 'portal/confirmation.html'
    context_object_name = 'posts'
    login_url = '/login/'

class Confirmation2DetailView(DetailView):
    model = Post
    template_name = 'portal/confirmation2.html'
    context_object_name = 'posts'
    login_url = '/login/'

class Job_SingleDetailView(DetailView):
    model = Post
    template_name = 'users/job_single.html'
    context_object_name = 'job_listing'
    login_url = '/login/'

class Job_SingleDetailView2(DetailView):
    model = Post
    template_name = 'users/job_single2.html'
    context_object_name = 'job_listing'
    login_url = '/login/'

class JobPostingView(View):
    def get(self, request):
        form = JobPostingForm()
        return render(request, 'post_job.html', {'form': form})
    
    def post(self, request):
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.employer = request.user
            job_listing.save()
            return redirect('job_listings')
        return render(request, 'post_job.html', {'form': form})

def about(request):
	return render(request, 'portal/about.html', {'title': 'About'})


@login_required
def applicants(request):
    context = {
        'applicants':Employer_Notification.objects.all(),
        'job_listings':Post.objects.all(),
        # Get applicant profiles associated with the job listings
        'applicant_profiles':Profile.objects.all()
    }

    return render(request, 'portal/applicants_list.html', context)


@login_required
def apply_job(request, pk):
    post = Post.objects.filter(pk=pk).first()
    employer = post.author
    applicant1 = request.user.username
    if employer == applicant1:
        # employer can't apply to their own post
        return redirect('post-detail', pk=pk)

    # create notification object and save to database
    notification = Employer_Notification.objects.create(
        user=employer,
        message=f'New application received for job post {post.title}.',
        description = post.description,
        location = post.location,
        is_active = post.is_active,
        company_name = post.company_name,
        title = post.title,
        applicant = applicant1,
        application_status = post.application_status
    )

    # set notification_sent flag to True and save post object
    post.notification_sent = True
    post.save()

    return redirect(reverse('portal-confirmation1') + f'?notification_sent=True', args=[post.pk])

    
def blog(request):
	return render(request, 'portal/blog.html', {'title': 'Blog'})

def blog_single(request):
	return render(request, 'portal/blog_single.html', {'title': 'Blog_Single'})


@login_required
def confirmation(request, pk):
    if pk:
        confirm = Post.objects.filter(pk=pk)
    args = {'confirm':confirm}
    return render(request, 'portal/confirmation.html', args, {'title': 'Confirmation'})


def confirmation1(request):
	messages.success(request, f'A notification has been sent to the employer.')
	return render(request, 'portal/confirmation1.html', {'title': 'Confirmation1'})


def confirmation2(request, pk):
    if pk:
        confirm = JobListing.objects.filter(pk=pk)
    args = {'confirm':confirm}
    return render(request, 'portal/confirmation2.html', args, {'title': 'Confirmation'})


def contact(request):
	return render(request, 'portal/contact.html', {'title': 'Contact'})

@login_required
def delete_job(request, pk):
    job = Post.objects.get(pk=pk)

    # Check if the logged-in user is the owner of the job
    if job.author != request.user:
        messages.error(request, 'You are not authorized to delete this job.')
        return redirect('job_listings')

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('job_listings')

    context = {'job': job}
    return render(request, 'portal/delete_job.html', context)



@login_required
def employer_response(request, title):
    notif = Employer_Notification.objects.filter(title=title).first()
    employee = notif.user
    employer1 = request.user.username
    if employee == employer1:
        # employer can't apply to their own post
        return redirect('post-detail', title=title)

    # create notification object and save to database
    e_notification = Employee_Notification.objects.create(
        user=employee,
        message=f'New application received for job notif {notif.title}.',
        description = notif.description,
        location = notif.location,
        is_active = notif.is_active,
        company_name = notif.company_name,
        title = notif.title,
        employer = employer1,
        application_status = notif.application_status
    )

    # set notification_sent flag to True and save post object
    notif.notification_sent = True
    notif.save()

    return redirect(reverse('portal-confirmation1') + f'?notification_sent=True', args=[notif.title])


def faq(request):
	return render(request, 'portal/faq.html', {'title': 'FAQ'})

def gallery(request):
	return render(request, 'portal/gallery.html', {'title': 'Gallery'})


def job_listings(request):
    context = {
          'job_listings':Post.objects.all()
    }
    return render(request, 'users/job_listings.html', context)


def login(request):
	return render(request, 'portal/login.html', {'title': 'Login'})

    
def notifications(request):
    return redirect(reverse(request, 'jobs/notification_list.html'))

@login_required
def employer_notifications(request):
    concept = {
        'notifications':Employer_Notification.objects.all(),
        'job_listings':Post.objects.all()
    }

    return render(request, 'portal/notifications_list.html', concept)

@login_required
def employee_notifications(request):
    concept = {
        'e_notifications':Employee_Notification.objects.all(),
        'job_listings':Post.objects.all()
    }

    return render(request, 'portal/notifications_list.html', concept)

'''
@login_required
def employee_notifications(request):
    notification2 = Employee_Notification.objects.filter(employee=request.user.employee)
    return redirect(reverse(request, 'portal/notification_list.html', {'notification2': notification2}))
'''

def portfolio(request):
	return render(request, 'portal/portfolio.html', {'title': 'Portfolio'})

def portfolio_single(request):
	return render(request, 'portal/portfolio_single.html', {'title': 'Portfolio Single'})	

def register(request):
	return render(request, 'portal/register.html', {'title': 'Register'})

def service_single(request):
	return render(request, 'portal/service_single.html', {'title': 'Service Single'})

def services(request):
	return render(request, 'portal/services.html', {'title': 'Services'})

def testimonials(request):
	return render(request, 'portal/testimonials.html', {'title': 'Testimonials'})

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        if searched:
            results = Post.objects.filter(title__contains=searched)
        else:
            results = []
        return render(request, 'portal/search_results.html', {'searched': searched, 'results': results})

    return render(request, 'portal/search_results.html', {})


def search_emp(request):
    if request.method == "POST":
        searched_emp = request.POST.get('searched_emp')
        if searched_emp:
            results_emps = Employee.objects.filter(username__contains=searched_emp)
        else:
            results_emps = []
        return render(request, 'portal/search_results.html', {'searched_emp': searched_emp, 'results_emps': results_emps})

    return render(request, 'portal/search_results.html', {})




'''user
    if request.method == 'POST':
        query = request.POST.get('query')

    if query:
        results = Post.objects.filter(Q(title__icontains=query))
    else:
        results = []

    if results:
        print(results)
    
    else:
         print("hello")

    return render(request, 'portal/search_results.html', {'results': results})
    '''



def posts(request):
    posts = Post.objects.all()
    return render(request, 'portal/posts.html', {'posts': posts})