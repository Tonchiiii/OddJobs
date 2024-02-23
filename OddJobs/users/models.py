from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    location = models.CharField(max_length=200, blank=False, null=False, default='')
    contact_number = models.CharField(max_length=20, blank=False, null=False, default='')
    email = models.EmailField(blank=False, null=False, default='')
    #is_employer = models.BooleanField(default=False)  # Add the is_employer field

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        super(Profile, self).save(*args, **kwargs)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # Add other fields as needed

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.first_name:
            self.first_name = self.user.first_name
        if not self.last_name:
            self.last_name = self.user.last_name
        super().save(*args, **kwargs)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    username = models.CharField(max_length=150, unique=True, default='')  # Inherited from User

    # Add other fields as needed

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.username
        if not self.first_name:
            self.first_name = self.user.first_name
        if not self.last_name:
            self.last_name = self.user.last_name
        super().save(*args, **kwargs)


class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.username} Location'

class UserContactNum(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} Contact Number'
    
class UserFirstName(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username}'
    
class UserLastName(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username}'
    
class UserEmail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return f'{self.user.username}'