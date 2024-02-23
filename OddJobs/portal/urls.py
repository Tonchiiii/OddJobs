from django.urls import path
from .views import PostListView, PostDetailView, ConfirmationDetailView, Confirmation2DetailView, Job_SingleDetailView, Job_SingleDetailView2
from jobs.views import EmployerNotificationListView, EmployeeNotificationListView
from users.views import Employee_ProfileDetailView
from . import views
from users import views as users_views


urlpatterns = [
    path('', PostListView.as_view(), name='portal-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('about/', views.about, name='portal-about'),
    path('applicants/', views.applicants, name='portal-applicants'),
    path('apply_job/<int:pk>/', views.apply_job, name='portal-apply_job'),
    path('employer_response/<str:title>/', views.employer_response, name='portal-employer_response'),
    path('blog/', views.blog, name='portal-blog'),
    path('blog_single/', views.blog_single, name='portal-blog_single'),
    path('confirmation1/', views.confirmation1, name='portal-confirmation1'),
    path('confirmation/<int:pk>/', ConfirmationDetailView.as_view(), name='portal-confirmation'),
    path('confirmation2/<int:pk>/', Confirmation2DetailView.as_view(), name='portal-confirmation2'),
    path('contact/', views.contact, name='portal-contact'),
    path('delete_job/<int:pk>/', views.delete_job, name='delete_job'),
    path('employee_notifications/', views.employee_notifications, name='portal-notifications2'),
    path('employer_notifications/', views.employer_notifications, name='portal-notifications1'),
    path('employee_profile/<int:pk>/', Employee_ProfileDetailView.as_view(), name='employee_profile'),
    path('faq/', views.faq, name='portal-faq'),
    path('gallery/', views.gallery, name='portal-gallery'),
    path('job_listings/', views.job_listings, name='job_listings'),
    path('job_single/<int:pk>/', Job_SingleDetailView.as_view(), name='portal-job_single'),
    path('job_single2/<int:pk>/', Job_SingleDetailView2.as_view(), name='portal-job_single2'),
    path('login/', views.login, name='portal-login'),
    path('payment_page/', users_views.payment_page, name='payment_page'),
    path('payment_post/', users_views.payment_post, name='payment_post'),
    path('portfolio/', views.portfolio, name='portal-portfolio'),
    path('portfolio_single/', views.portfolio_single, name='portal-portfolio_single'),
    path('posts/', views.posts, name='posts'),
    path('post_job/', users_views.post_job, name='post_job'),
    path('register/', views.register, name='portal-register'),
    path('search/', views.search, name='portal-search'),
    path('search_emp/', views.search_emp, name='portal-search_emp'),
    path('service_single/', views.service_single, name='portal-service_single'),
    path('services/', views.services, name='portal-services'),
    path('payment_success/', users_views.payment_success, name='payment_success'),
    path('payment_failed/', users_views.payment_failed, name='payment_failed'),
    path('testimonials/', views.testimonials, name='portal-testimonials'),
]