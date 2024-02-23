from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse

User = get_user_model()

class Job(models.Model):
    # ... fields ...
    pass

class JobApplication(models.Model):
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)

    def get_absolute_url(self):
        # Use reverse to generate the URL for the employer's notification page
        return reverse('employer_notifications')

    def send_notification(self):
        # Create a Notification object and save it to the database
        employer = self.job.employer
        notification = Notification(
            user=employer,
            message=f'{self.applicant_name} applied for {self.job.title}.',
            link=self.get_absolute_url()
        )
        notification.save()


class JobListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


User = get_user_model()

class Employer_Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.CharField(max_length=200, null=True, default=None)
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=200)
    description = models.TextField(default=None)
    company_name = models.CharField(max_length=200, null=True, default=None)
    location = models.CharField(max_length=200, null=True, default=None)
    is_active = models.BooleanField(default=True)
    application_status = models.CharField(max_length=100, default=None)
    message = models.TextField(max_length=200, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Set the application_status field to "PENDING" if it's a new object
        if not self.pk:
            self.application_status = "PENDING"
        super().save(*args, **kwargs)

'''
    def save(self, *args, **kwargs):
        # Set the applicant field to the username of the user who applies for the job
        self.applicant = self.user.applicant
        super().save(*args, **kwargs)
'''    
class Employee_Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.CharField(max_length=200, null=True, default=None)
    link = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default=None)
    company_name = models.CharField(max_length=200, null=True, default=None)
    location = models.CharField(max_length=200, null=True, default=None)
    is_active = models.BooleanField(default=True)
    application_status = models.CharField(max_length=100, default=None)
    message = models.TextField(max_length=200, default=None)
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Set the application_status field to "PENDING" if it's a new object
        if not self.pk:
            self.application_status = "ONGOING"
        super().save(*args, **kwargs)