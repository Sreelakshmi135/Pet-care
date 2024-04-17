from django.db import models
from django.contrib.auth.models import User

class Userdetails(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=6)
    role = models.CharField(max_length=10, default="user")
    
    def __str__(self):
        return f'{self.full_name}'
    
class bookingcart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField()
    petname = models.CharField(max_length=50, null=False, blank=False)
    pettype = models.CharField(max_length=50, null=False, blank=False)    
    petbreed = models.CharField(max_length=50, null=False, blank=False)
    petage = models.CharField(max_length=50, null=False, blank=False) 
    petservice = models.CharField(max_length=50, null=False, blank=False) 
    petgender = models.CharField(max_length=50, null=False, blank=False) 
    bookingdate = models.CharField(max_length=10, null=False, blank=False) 
    bookingtime = models.CharField(max_length=5, null=False, blank=False)

class Service(models.Model):
    service_name = models.CharField(max_length=255)
    service_charge = models.IntegerField()
    image = models.ImageField(upload_to='services/')
    service_description = models.TextField()

    def __str__(self):
        return self.service_name

class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  # You can adjust the max length as needed
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)  # Assuming you want usernames to be unique
    password = models.CharField(max_length=100)
    specialization = models.CharField(max_length=255)
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Boarding(models.Model):
    boarding_type = models.CharField(max_length=255)
    boarding_charge = models.IntegerField()
    image = models.ImageField(upload_to='boarding/')
    boarding_description = models.TextField()
    is_available = models.BooleanField(default=True)  # New field for availability status


class PetBoarding(models.Model):
    type = models.CharField(max_length=50, null=False, blank=False)    
    breed = models.CharField(max_length=50, null=False, blank=False)
    age = models.CharField(max_length=50, null=False, blank=False) 
    name = models.CharField(max_length=50, null=False, blank=False)
    gender = models.CharField(max_length=7, null=False, blank=False)
    service = models.CharField(max_length=50, null=False, blank=False)
    email_id = models.CharField(max_length=50, null=False, blank=False)
    user_name = models.CharField(max_length=50, null=False, blank=False)
    pickup_date = models.DateField(null=False, blank=False)
    drop_date = models.DateField(null=False, blank=False)
    appointment_time = models.TimeField(null=False, blank=False)
    charge = models.CharField(max_length=50, null=False, blank=False)
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    postal_code = models.CharField(max_length=6, null=False, blank=False)
    
    def __str__(self):
        return f"{self.name}-{self.type}"
    
class Vaccination(models.Model):
    vaccination_type = models.CharField(max_length=255,null=True,blank=True)
    vaccination_charge = models.IntegerField( null=True,blank=True)
    image = models.ImageField(upload_to='vaccination/')
    vaccination_description = models.TextField(null=True,blank=True)

class PetVaccination(models.Model):
    pet_name = models.CharField(max_length=100)
    vaccination_name = models.CharField(max_length=100)
    previous_vaccination_date = models.DateField()
    previous_vaccination_name = models.CharField(max_length=100)
    next_vaccination_date = models.DateField()
    vet_name = models.CharField(max_length=100)
    additional_notes = models.TextField()


class LeaveApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)  
    user_name = models.CharField(max_length=100)  
    leave_date = models.DateField()
    leave_type = models.CharField(max_length=20)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='Pending')
