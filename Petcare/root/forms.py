from django.forms import ModelForm
from .models import Userdetails
from .models import bookingcart
from .models import PetService


class Userform(ModelForm):
    class Meta:
        model=Userdetails
        fields= [
             "full_name",
             "email",
             "phone",
             "username" ,
             "password",
        ] 
class bookingcartform(ModelForm):
    class Meta:
        model=bookingcart
        fields="__all__"
        


PetService.objects.all()
        