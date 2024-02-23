from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import JobApplication, JobListing, Employee_Notification, Employer_Notification
from portal.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin


class EmployeeNotificationListView(LoginRequiredMixin, ListView):
    model = Employee_Notification
    context_object_name = 'e_notification'
    template_name = 'portal/notifications_list.html'
    login_url = '/login/'

    def get_queryset(self):
        return Employee_Notification.objects.filter(user=self.request.user)
    

class EmployerNotificationListView(LoginRequiredMixin, ListView):
    model = Employer_Notification
    context_object_name = 'notification'
    template_name = 'portal/notifications_list.html'
    login_url = '/login/'

    def get_queryset(self):
        return Employer_Notification.objects.filter(user=self.request.user)
    

class JobApplicationCreateView(CreateView):
    model = JobApplication
    fields = ['applicant_name']
    
    def form_valid(self, form):
        job = Job.objects.get(pk=self.kwargs['pk'])
        form.instance.job = job
        response = super().form_valid(form)
        self.object.send_notification()
        return response



# Create your views here.
