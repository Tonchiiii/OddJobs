from django.contrib import admin
from .models import JobListing, JobApplication, Employer_Notification, Employee_Notification
from portal.models import Post

admin.site.register(Post)
admin.site.register(JobListing)
admin.site.register(JobApplication)
admin.site.register(Employee_Notification)
admin.site.register(Employer_Notification)

