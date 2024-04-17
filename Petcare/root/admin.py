from django.contrib import admin
from . import models
# Register your models here

admin.site.register(models.Userdetails)
admin.site.register(models.bookingcart)
admin.site.register(models.Staff)
admin.site.register(models.Service)
admin.site.register(models.Boarding)
admin.site.register(models.PetBoarding)
admin.site.register(models.Vaccination)
admin.site.register(models.PetVaccination)
admin.site.register(models.LeaveApplication)