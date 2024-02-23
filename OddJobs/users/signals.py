from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, UserLocation, UserContactNum, UserFirstName, UserLastName, UserEmail

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
        if instance.profile.first_name:
            UserFirstName.objects.update_or_create(user=instance, first_name=instance.profile.first_name)
        if instance.profile.last_name:
            UserLastName.objects.update_or_create(user=instance, last_name=instance.profile.last_name)
        if instance.profile.location:
            UserLocation.objects.create(user=instance, location=instance.profile.location)
        if instance.profile.contact_number:
            UserContactNum.objects.create(user=instance, contact_number=instance.profile.contact_number)
        if instance.profile.email:
            UserEmail.objects.update_or_create(user=instance, email=instance.profile.email)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    if instance.profile.first_name:
        UserFirstName.objects.update_or_create(user=instance, first_name=instance.profile.first_name)
    if instance.profile.last_name:
        UserLastName.objects.update_or_create(user=instance, last_name=instance.profile.last_name)
    if instance.profile.location:
        UserLocation.objects.update_or_create(user=instance, location=instance.profile.location)
    if instance.profile.contact_number:
        UserContactNum.objects.update_or_create(user=instance, contact_number=instance.profile.contact_number)
    if instance.profile.email:
        UserEmail.objects.update_or_create(user=instance, email=instance.profile.email)