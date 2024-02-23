from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	company_name = models.CharField(max_length=200, null=True, default=None)
	location = models.CharField(max_length=200, null=True, default=None)
	salary = models.CharField(max_length=100, null=True, default=None)
	date_posted = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	applicant = models.CharField(max_length=200, default=None, null=True)
	application_status = models.CharField(max_length=100, default=None)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		'''
		# Set the applicant field to the username of the user who applies for the job
		self.applicant = self.author.username
		'''
		if not self.application_status:
			self.application_status = 'PENDING'
		super().save(*args, **kwargs)
	
	    
