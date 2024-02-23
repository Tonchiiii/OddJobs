from django.urls import path
from .views import JobPostingView, JobListView
from . import views

urlpatterns = [
    path('post_job/', JobPostingView.as_view(), name='post_job'),
    #path('jobs/', JobListView.as_view(), name='job_listings'),
]