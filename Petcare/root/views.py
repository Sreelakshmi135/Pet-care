import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login  # Rename the 'login' function
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from.models import *
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import Staff
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, bookingcart
from django.shortcuts import redirect
from datetime import date
from django.core.mail import send_mail
from .models import Service
from django.contrib import messages
from .models import Review
from django.http import HttpResponseForbidden
from .models import bookingcart
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from .models import Boarding, PetBoarding, Vaccination, PetVaccination
from .models import LeaveApplication
from django.core.exceptions import ObjectDoesNotExist


from django.shortcuts import render, redirect

@never_cache
def index(request):
    return render(request, "home/index.html")

@csrf_exempt
def success(request):
    return render(request,"home/sucess.html")
    

def login(request):  # Renamed the view function
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
       
  
        if user is not None:
            auth_login(request, user)  # Use the renamed 'auth_login' function
            request.session['username'] = user.username
            if username == 'sree' and password =='Sree123@':
                return redirect('dashboard')
            try:
                staff = Staff.objects.get(username=username)
                if staff.password == password:
                    return redirect("new")  # Redirect to staff_profile for Technicians
            except Staff.DoesNotExist:
                pass  # No Technician with this username

            
            return redirect('user_index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    response = render(request, "login/login.html")
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
             
        
@never_cache
def signin(request):
    if request.method == "POST":        
        full_name = request.POST['full-name']
        phone_num = request.POST['phone']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        
        user_obj=Userdetails(full_name=full_name,email=email,phone=phone_num,username=username,password=password)
        user_obj.save()
        return redirect('login')
    return render(request, "signin/signin.html")


        
    

# Other view functions...

@never_cache
def service(request):
    return render(request,"home/service.html")

def adminservices(request):
    return render(request,"home/adminservices.html")
#  return HttpResponse("servicepage")

@never_cache
def about(request):
    return render(request,"home/about.html")

@never_cache
def contact(request):
    return render(request,"home/contact.html")

def blog(request):
    return render(request,"home/blog.html")

@never_cache    
@login_required(login_url='login')
def new(request):
    return render(request,"home/new.html")

def book(request):
    return render(request,"login/book.html")


from django.shortcuts import render

def appointment_form(request):
    if request.method == 'POST':
        # Handle form submission
        # You can access the selected pet type and breed using request.POST

     return render(request, 'new.html')


@never_cache    
@login_required(login_url='login')
def user_index(request):
    if 'username' in request.session:
        services = Service.objects.all()
        context = {
            'services': services,
        }
        response = render(request,"user_index/user_index.html", context)
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')
    
@never_cache    
@login_required(login_url='login')
def booking(request, service_name):
    if request.method == "POST":
        pettype = request.POST.get("petType1")
        name = request.POST.get("name1")
        age = request.POST.get("age1")
        email  = request.POST.get("email")
        vaccinated = request.POST.get("vaccinated1")
        breed = request.POST.get("breed1")
        gender = request.POST.get("gender1")
        petservice = request.POST.get("pet-service")
        bookingdate = request.POST.get("preferred-date")
        appointmenttime = request.POST["appointment_time"]
        
        appointment = bookingcart(petname=name,pettype=pettype,
                                  petbreed=breed,petage=age,email=email,
                                  petservice=petservice,petgender=gender,
                                  bookingdate=bookingdate,bookingtime=appointmenttime)
        appointment.save()
        # print(name,pettype,age,vaccinated,breed,gender,petservice,bookingdate,appointmenttime)     #,age,vaccinated,breed,gender,petservice,bookingdate,appointmenttime
        
    today = date.today()
    return render(request,"home/booking.html",{'today': today})

def user_bookings(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Query bookings for the current user
        user_bookings = bookingcart.objects.filter(user=request.user)

        return render(request, 'home/user_bookings.html', {'user_bookings': user_bookings})
    else:
        # Redirect to login page or handle unauthenticated users
        return render(request, 'login.html') 


@never_cache
def logout(request):
    auth.logout(request)
    return redirect('/')
    # return HttpResponse("Logged out")
    
def reg(request):
    return render(request,"new/new.html")
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, HttpResponse
from .models import bookingcart

@never_cache    
@login_required(login_url='login')
def staff_index(request):  
    

    # Retrieve all booking instances with related Userdetails
    bookings = bookingcart.objects.select_related('user').all()
    context = {'bookings': bookings}
    return render(request, "home/staff_index.html", context)

    bookings = bookingcart.objects.all()
    
    return render(request, 'home/staff_index.html', {'bookings': bookings})
    send_mail(
            'We Bare Bears',
            f'Dear {full_name},\n\nYou have been added as a staff member . Your username is {username} and password is {password}. '
            f'Please log in with these credentials using the following link:\n' \
           
            f'Remember to update your profile and change the temporary password provided.\n\n' \
            f'Thank you! Team Paws and Tails',

           
            'sreelakshmip2024b@mca.ajce.in',  # Replace with your email address
            [email],  # Use the staff member's email address
            fail_silently=False,
        )

    return redirect('staffs')  # Redirect to the staff list view




def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def check_username_availability(request):
    username = request.GET.get("username")
    try:
        user = User.objects.get(username=username)
        available = False
    except User.DoesNotExist:
        available = True
    return JsonResponse({"available": available})


def check_email_availability(request):
    email = request.GET.get('email', None)
    data = {}
    if email:
        # Check if the email exists in the database using Django's User model
        if User.objects.filter(email=email).exists():
            data['available'] = False
        else:
            data['available'] = True
    else:
        data['error'] = 'Invalid request'
    return JsonResponse(data)

    
@never_cache 
@login_required(login_url='login')
def userreg(request):
    if request.user.is_superuser:
        users = Userdetails.objects.exclude(username='sree')  # Query the custom Userdetails model
        return render(request, "home/userreg.html", {"users": users})
    return redirect("index")



def dashboard(request):
    if request.user.is_superuser:
        recent_users = User.objects.filter(is_superuser=False).order_by('-date_joined')[:10]  # Query the 10 most recent non-superuser users
        return render(request, "home/dashboard.html", {"recent_users": recent_users})
    return redirect("index")
def acceptTerms(request):
    return render(request,"home/acceptTerms.html")
   
def profile_update(request):
    return render(request,"home/profile_update.html")
def doctors(request):
    return render(request,"home/doctors.html")
def doctorsone(request):
    return render(request,"home/doctorsone.html")
def doctorstwo(request):
    return render(request,"home/doctorstwo.html")
def doctorsthree(request):
    return render(request,"home/doctorsthree.html")
def update_profile(request):
    return render(request,"home/update_profile.html")

def update_profile(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        # Get other fields if needed

        # Update the user's profile
        user = request.user
        user.username = full_name
        user.email = email
        # Update other fields

        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile_update')

    return render(request,"home/update_profile.html")

@never_cache    
@login_required(login_url='login')
def cart(request):
    if request.method == "POST":      
        amount= 50000
        currency= 'INR'
        client = razorpay.Client(
            auth=("rzp_test_Y2yeTt6Auyhn36","ERXOhu8WY1QJ4ln75l2CEHjU"))
        payment = client.order.create({'amount':amount, 'currency': 'INR', 'payment_capture': '1'})
        return redirect('cart')  # Redirect to a success page

    return render(request, "home/cart.html")
    # This view will render the 'cart.html' page
  

def confirmbooking(request, boarding_id):
    boarding = get_object_or_404(Boarding, pk=boarding_id)
    print("Boarding Charge:", boarding.boarding_charge)  # Debugging print statement
    # This view will render the 'confirmbooking.html' page
    return render(request, 'home/confirmbooking.html', {'boarding': boarding})


def add_service(request):
    if request.method == 'POST':
        service_name = request.POST['service_name']
        service_charge = request.POST['service_charge']
        image = request.FILES['image']
        service_description = request.POST['service_description']

        service = Service(service_name=service_name, service_charge=service_charge, image=image, service_description=service_description)
        service.save()
        return redirect('service_list')

    return render(request, 'home/add_service.html')



def service_list(request):
    services = Service.objects.all()
    return render(request, 'home/service.html', {'services': services})

@never_cache 
@login_required(login_url='login')
def newservice(request):
    return render(request,"home/newservice.html")


@never_cache 
@login_required(login_url='login')
def add_staff(request):
    if request.method == "POST":
        # Get the form data
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
    
        # Perform validation checks
        errors = {}
        if not full_name:
            errors['full_name'] = 'Full Name is required'
        if not username:
            errors['username'] = 'Username is required'
        # Add more validation checks as needed

        # Check for validation errors
        if errors:
            return render(request, 'home/add_staff.html', {'errors': errors})
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=full_name.split()[0],  # Assuming the first word is the first name
            last_name=' '.join(full_name.split()[1:]),
            is_staff = True# Remaining words as the last name
        )

        # Create a new Staff object and save it to the database
        staff = Staff(
            full_name=full_name,
            username=username,
            password=password,  # Note: Storing passwords directly is not secure, consider hashing
            email=email,
        )
        staff.save()
        
        # Send a welcome email
        send_mail(
            'We Bare Bears',
            f'Dear {full_name},\n\nYou have been added as a staff member . Your username is {username} and password is {password}. '
            f'Please log in with these credentials using the following link:\n' \
           
            f'Remember to update your profile and change the temporary password provided.\n\n' \
            f'Thank you! Team Paws and Tails',

           
            'sreelakshmip2024b@mca.ajce.in',  # Replace with your email address
            [email],  # Use the staff member's email address
            fail_silently=False,
        )

        return redirect('staffs')  # Redirect to the staff list view

    else:
        return render(request, 'home/add_staff.html')
    
def staffs(request):
    staff_data = Staff.objects.all()
    return render(request, 'home/staffs.html', {'staff_data': staff_data})

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    
    if request.method == 'POST':
        staff.delete()
    
    return redirect('staff_list') 
def staff_list(request):
    staff_data = Staff.objects.all()  # Query the staff data from your database
    return render(request, 'home/staff_list.html', {'staff_data': staff_data})

            
def newcart(request):
    return render(request,"home/newcart.html")
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'GET':
        service.delete()
    
    return redirect('service_list')  
def accept_terms(request):
    return redirect(request,'home/cart.html ') 
def backup(request):
    # You can retrieve the total amount from the request and pass it to the template
   total_amount = request.GET.get('totalAmount', 'total')

    # Render the HTML template and pass the total_amount variable to the template
   return render(request, 'home/backup.html', {'total_amount': total_amount})

def feedback_thankyou(request):
    return render(request,'home/feedback_thankyou.html ') 

def adminfeedback(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'home/adminfeedback.html', {'feedback_list': feedback_list})

    
def delete_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    service.delete()
    return redirect('service_list')  # Redirect to the service list page

def edit_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    
@login_required
def submit_feedback(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        if feedback_message:
            Feedback.objects.create(user=request.user, message=feedback_message)
            # You can add additional logic here (e.g., sending a confirmation email)
            return redirect('home/feedback_thankyou')
    return render(request, 'home/feedback_form.html')



@login_required(login_url='login')
def review(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # Get the user instance
        try:
            user = get_user_model().objects.get(pk=request.user.pk)
        except get_user_model().DoesNotExist:
            # Handle the case where the user does not exist
            return HttpResponseForbidden("User not found")

        # Create a new review
        review = Review(user=user, comment=comment, rating=rating)
        review.save()

        messages.success(request, 'Review submitted successfully!')
        return redirect('user_index')
    else:
        return HttpResponseForbidden("Invalid request method")

# def new(request):
#     if request.method == 'POST':
#         # Process your form submission
#         # ...

#         # Calculate the total amount using the defined function
#         total_amount = calculate_total_amount(request.POST)

#         # Pass the total amount to the new page
#         return render(request, 'total_amount_page.html', {'total_amount': total_amount})

#     # Handle GET requests here (if needed)
#     return HttpResponse("Please use a POST request to submit the form.")
def bookingconfirmation(request):
    
    
    booking = bookingcart.objects.latest('id')

    # Pass the relevant details to the template
    context = {
        
       
    }
    return render(request, 'bookingconfirmation.html', context)

def staff_service(request):
    if 'username' in request.session:
        services = Service.objects.all()
        context = {
            'services': services,
        }
        response = render(request,"home/staff_service.html", context)
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')

@never_cache 
@login_required(login_url='login')
def alert(request):
    return render(request,'home/alert.html ')

@never_cache 
@login_required(login_url='login')
def boarding_appointment(request):
    if request.method == "POST":
        # Extracting data from the POST request
        petType1 = request.POST.get('petType1')
        name1 = request.POST.get('name1')
        age1 = request.POST.get('age1')
        breed1 = request.POST.get('breed1')
        gender1 = request.POST.get('gender1')
        pet_service = request.POST.get('pet-service')
        email = request.POST.get('email')
        username = request.POST.get('username')
        pickup_date = request.POST.get('pickup-date')
        drop_date = request.POST.get('drop-date')
        charge = request.POST.get('charge')
        street = request.POST.get('street') 
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postalCode')
        appointment_time = request.POST.get('appointment_time')
        boarding_id = request.session.get('boarding_id')
        print("hhhhhhhhhhhhh",boarding_id)
        
        # Creating a new PetBoarding object
        pet_boarding = PetBoarding(
            type=petType1, 
            name=name1, 
            age=age1, 
            breed=breed1, 
            gender=gender1, 
            service=pet_service, 
            email_id=email, 
            user_name=username, 
            pickup_date=pickup_date, 
            drop_date=drop_date, 
            appointment_time=appointment_time,
            charge=charge,
            street=street,
            city=city,
            state=state,
            postal_code=postal_code,
        )
        pet_boarding.save()
        
        # Redirecting to the payment page with the boarding ID
        
        return redirect('payment', boarding_id=boarding_id)

       

@never_cache    
@login_required(login_url='login')
def boardingapp(request, boarding_id):
    boardings = get_object_or_404(Boarding, pk=boarding_id)
    request.session['boarding_id'] = boarding_id
    
    return render(request, 'home/boardingapp.html ', {'boarding': boardings})



@never_cache 
@login_required(login_url='login')
def boarding_list(request):
    # Fetch all Boarding instances from the database
    boardings = Boarding.objects.all()

    return render(request, 'home/boarding_list.html', {'boardings': boardings})


@never_cache 
@login_required(login_url='login')
def boarding_list1(request):
    # Fetch all Boarding instances from the database
    boardings = Boarding.objects.all()

    return render(request, 'home/boarding_list1.html', {'boardings': boardings})

def delete_boarding(request, boarding_id):
    boarding = get_object_or_404(Boarding, id=boarding_id)
    
    # Update the availability status instead of deleting
    boarding.is_available = False
    boarding.save()

    # Redirect to the same page or wherever you want
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def make_available(request, boarding_id):
    boarding = get_object_or_404(Boarding, id=boarding_id)
    
    # Update the availability status to True
    boarding.is_available = True
    boarding.save()

    # Redirect to the same page or wherever you want
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def make_unavailable(request, boarding_id):
    boarding = get_object_or_404(Boarding, id=boarding_id)
    
    # Update the availability status to True
    boarding.is_available = False
    boarding.save()

    # Redirect to the same page or wherever you want
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@never_cache 
@login_required(login_url='login')
def boardingindex(request):
    boarding_entries = PetBoarding.objects.all()
    return render(request, 'home/boardingindex.html', {'boarding_entries': boarding_entries})

@never_cache    
@login_required(login_url='login')
def boarding_detail(request, boarding_id):
    boarding = get_object_or_404(PetBoarding, pk=boarding_id)
    return render(request, 'home/boarding_detail.html', {'boarding': boarding})

@never_cache    
@login_required(login_url='login')
def Petcare_services(request):
    return render(request,"home/Petcare_services.html")
# def payment(request, boarding_id):
#     boarding = PetBoarding.objects.get(pk=boarding_id)
#     return render(request, 'payment.html', {'boarding': boarding})

@never_cache    
@login_required(login_url='login')
def payment(request, boarding_id):
    boarding = get_object_or_404(Boarding, pk=boarding_id)

    if request.method == "POST":  
        # Payment processing logic
        amount = 50000
        order_currency = 'INR'
        client = razorpay.Client(auth=("rzp_test_Y2yeTt6Auyhn36", "ERXOhu8WY1QJ4ln75l2CEHjU"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        
        # You may want to save the payment information or handle success/failure here

        # Redirect to a success page or perform additional actions as needed
        return redirect('confirmbooking')

    return render(request, 'home/payment.html', {'boarding': boarding})
    # This view will render the 'cart.html' page
    
def send_verification_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        # Send email
        send_mail(
            'Verification Email',
            'Your account has been verified.',
            'sreelakshmip2024b@mca.ajce.in',  # Set your sender email address
            [email],
            fail_silently=False,
        )

        return JsonResponse({'status': 'Email sent successfully'})

    return JsonResponse({'status': 'Invalid request'}, status=400)
@never_cache    
@login_required(login_url='login')
def add_vaccination(request):
    if request.method == 'POST':
        # Process the form data and save to the database
        vaccination_type = request.POST.get('vaccination_type')
        vaccination_charge = request.POST.get('vaccination_charge')
        image = request.FILES.get('image')
        vaccination_description = request.POST.get('vaccination_description')

        vaccination = Vaccination(
            vaccination_type=vaccination_type,
            vaccination_charge=vaccination_charge,
            image=image,
            vaccination_description=vaccination_description
        )
        vaccination.save()  # Corrected: Call save() with parentheses

        # Redirect after successful form submission
        return redirect('vaccination_list1')

    return render(request, 'home/add_vaccination.html')



@never_cache    
@login_required(login_url='login')
def add_boarding(request):
    if request.method == 'POST':
        # Process the form data and save to the database
        boarding_type = request.POST.get('boarding_type')
        boarding_charge = request.POST.get('boarding_charge')
        image = request.FILES.get('image')
        boarding_description = request.POST.get('boarding_description')

        boarding = Boarding(
            boarding_type=boarding_type,
            boarding_charge=boarding_charge,
            image=image,
            boarding_description=boarding_description
        )
        boarding.save()  # Corrected: Call save() with parentheses

        # Redirect after successful form submission
        return redirect('boarding_list1')

    return render(request, 'home/add_boarding.html')


@never_cache 
@login_required(login_url='login')
def vaccination_list1(request):
    vaccinations = Vaccination.objects.all()
    return render(request, 'home/vaccination_list1.html', {'vaccinations': vaccinations})

def live_search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        results = Boarding.objects.filter(boarding_type__icontains=query)
        data = [
            {
                'id': boarding.id,
                'type': boarding.boarding_type,
                'charge': boarding.boarding_charge,
                'description': boarding.boarding_description,
                'image_url': boarding.image.url if boarding.image else '',
            }
            for boarding in results
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

# def live_search(request):
#     if request.method == 'GET':
#         query = request.GET.get('q', '')
#         results = Vaccination.objects.filter(vaccination_type__icontains=query)
#         data = [
#             {
#                 'id': vaccination.id,
#                 'type': vaccination.vaccination_type,
#                 'charge': vaccination.vaccination_charge,
#                 'description': vaccination.vaccination_description,
#                 'image_url': vaccination.image.url if vaccination.image else '',
#             }
#             for vaccination in results
#         ]
#         return JsonResponse(data, safe=False)
#     return JsonResponse([], safe=False)

def delete_vaccination(request, vaccination_id):
    vaccination = get_object_or_404(Vaccination, id=vaccination_id)

    # Check if the request method is POST to confirm deletion
    if request.method == 'POST':
        vaccination.delete()
        return redirect('vaccination_list1')  

    return render(request, 'confirm_delete.html', {'vaccination': vaccination})


@never_cache 
@login_required(login_url='login')
def vaccination_list(request):
    vaccinations = Vaccination.objects.all()
    return render(request, 'home/vaccination_list.html', {'vaccinations': vaccinations})

def search_vaccinations(request):
    search_term = request.GET.get('search', '')
    vaccinations = Vaccination.objects.filter(vaccination_type__icontains=search_term)
    return render(request, 'home/vaccination_list1.html', {'vaccinations': vaccinations})

def image_detection(image_path):
    print(f"image_path:{image_path}")

    img = Image.open(image_path)


    model = timm.create_model('vgg19.tv_in1k', pretrained=True)
    model = model.eval()

    # get model specific transforms (normalization, resize)
    data_config = timm.data.resolve_model_data_config(model)
    transforms = timm.data.create_transform(**data_config, is_training=False)

    output = model(transforms(img).unsqueeze(0))  # unsqueeze single image into batch of 1

    top5_probabilities, top5_class_indices = torch.topk(output.softmax(dim=1) * 100, k=5)
    print(f"top5_probabilities:{top5_probabilities}")
    print(f"top5_class_indices:{top5_class_indices}")
    return top5_probabilities

def dragdrop(request):
    #after ssubmit button
    #render 
    image_path = r"C:/Pet care/Petcare/root/cat-3.jpg"
    # top5_probabilities  = image_detection(image_path)
    print(f"image_path:{image_path}")

    img = Image.open(image_path)


    model = timm.create_model('vgg19.tv_in1k', pretrained=True)
    model = model.eval()

    # get model specific transforms (normalization, resize)
    data_config = timm.data.resolve_model_data_config(model)
    transforms = timm.data.create_transform(**data_config, is_training=False)

    output = model(transforms(img).unsqueeze(0))  # unsqueeze single image into batch of 1

    top5_probabilities, top5_class_indices = torch.topk(output.softmax(dim=1) * 100, k=5)
    print(f"top5_probabilities:{top5_probabilities}")
    print(f"top5_class_indices:{top5_class_indices}")
    context = {
        top5_probabilities: "top5_probabilities"
    }
    
    return render(request,"home/dragdrop.html",context)

import requests
import os
API_URL = "https://api-inference.huggingface.co/models/timm/vgg19.tv_in1k"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
        
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# def result(request):
#     context ={}
#     if request.method == 'POST' and request.FILES.get('image'):
#         uploaded_image = request.FILES['image']
#         # Open a new file in binary write mode
#         with open(os.path.join("./", uploaded_image.name), 'wb+') as destination:
#             # Iterate through the uploaded image chunks and write them to the destination
#             for chunk in uploaded_image.chunks():
#                 destination.write(chunk)
#         print(f"llll:{uploaded_image.name}")

#         try:
#             results = query(uploaded_image.name)
#             results = list(results)
#             print(f"output:{results}")
            
#             label1 = results[0]['label']
#             score1 = results[0]['score']
#             print(label1)
#             print(score1)
#             context = {
#                 'label1': label1,
#                 'score1': score1,
#                 'results': results
#             }
#         except Exception as e:
#             print(e)
    
#     # This view will render the 'confirmbooking.html' page
#     return render(request, 'home/result.html', context)
def result(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        # Open a new file in binary write mode
        with open(os.path.join("./", uploaded_image.name), 'wb+') as destination:
            # Iterate through the uploaded image chunks and write them to the destination
            for chunk in uploaded_image.chunks():
                destination.write(chunk)
        print(f"llll:{uploaded_image.name}")

        try:
            results = query(uploaded_image.name)
            results = list(results)
            print(f"output:{results}")
            
            label1 = results[0]['label']
            score1 = results[0]['score']

            # Map score values to accuracy levels
            if score1 >= 0.3:
                accuracy_level = "High"
            elif score1 >= 0.2:
                accuracy_level = "Medium"
            else:
                accuracy_level = "Low"

            print(label1)
            print(score1)
            print(accuracy_level)

            context = {
                'label1': label1,
                'accuracy_level': accuracy_level,
                'results': results
            }
        except Exception as e:
            print(e)
    
    # This view will render the 'result.html' page
    return render(request, 'home/result.html', context)




@never_cache 
@login_required(login_url='login')
def Vacc(request):
    vaccinations = Vaccination.objects.all()
    if request.method == 'POST':
            # Retrieve data from the request
            pet_name = request.POST.get('petName')
            vaccination_name = request.POST.get('vaccineName')
            previous_vaccination_date = request.POST.get('previousVaccineDate')
            previous_vaccination_name = request.POST.get('previousVaccineName')
            next_vaccination_date = request.POST.get('nextVaccineDate')
            vet_name = request.POST.get('vetName')
            additional_notes = request.POST.get('additionalNotes')
            print(previous_vaccination_date)
            # Create a new instance of PetVaccination model
            pet_vaccination = PetVaccination(
                pet_name=pet_name,
                vaccination_name=vaccination_name,
                previous_vaccination_date=previous_vaccination_date,
                previous_vaccination_name=previous_vaccination_name,
                next_vaccination_date=next_vaccination_date,
                vet_name=vet_name,
                additional_notes=additional_notes
            )

            # Save the instance to the database
            pet_vaccination.save()

            # Redirect to a success page or render a success message
            return redirect('timer_clock')  # Adjust the URL as needed

    else:
        return render(request, 'home/Vacc.html')
    

@never_cache 
@login_required(login_url='login')
def timer_clock(request):
    return render(request, 'home/timer_clock.html')


@never_cache 
@login_required(login_url='login')
def VaccDetails(request):
    # Retrieve all instances of PetVaccination from the database
    vaccinations = PetVaccination.objects.all()

    # Pass the retrieved data to the template for rendering
    return render(request, 'home/VaccDetails.html', {'vaccinations': vaccinations})
def download_file(request):
    # Replace '/path/to/your/file/example.txt' with the actual path to the file
    file_path = '/path/to/your/file/example.txt'

    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        # Set the appropriate Content-Disposition header
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
def staff_leave_view(request):
    return render(request, 'home/Staff_leave.html')

def leave_application(request):
    if request.method == 'POST':
        staff_name = request.POST.get('userName')
        leave_dates = request.POST.getlist('leaveDate')
        leave_types = request.POST.getlist('leaveType')
        reasons = request.POST.getlist('reason')

        for leave_date, leave_type, reason in zip(leave_dates, leave_types, reasons):
            LeaveApplication.objects.create(
                user_name = staff_name,
                leave_date = leave_date,
                leave_type = leave_type,
                reason = reason
            )
        
        return redirect('index')  # Redirect to a success page
    else:
        return render(request, 'staff_leave.html')

def admin_leave_approval(request):
    leave_requests = LeaveApplication.objects.all()
    return render(request, 'home/admin_leave_approval.html', {'leave_requests': leave_requests})

def leave_approval_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        leave_ids = request.POST.getlist('leave_ids[]')

        if action == 'approve':
            LeaveApplication.objects.filter(pk__in=leave_ids).update(status='Approved')
        elif action == 'reject':
            LeaveApplication.objects.filter(pk__in=leave_ids).update(status='Rejected')

    return redirect('admin_leave_approval')
def staff_dashboard(request):
    return render(request, 'home/staff_dashboard.html')


