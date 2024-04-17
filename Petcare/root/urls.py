from django.urls import path
from . import views
from .views import cart
from .views import review
from django.contrib.auth import views as auth_views
from .views import user_bookings
from .views import send_verification_email
from .views import staff_leave_view



urlpatterns = [     
    path('',views.index,name="index"),  

    path('index/',views.index,name="index"),  
    path('login/',views.login,name="login"),
    path('signin/',views.signin,name="signin"),
    path('service/',views.service,name="service"),
    path('adminservices/',views.adminservices,name="adminservices"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),

    path('blog/',views.blog,name="blog"),
    path('new/',views.new,name="new"),
    path('user_index/',views.user_index,name="user_index"),
    path('book/',views.book,name="book"),
    path('booking/<str:service_name>/', views.booking, name='booking'),

    path('logout',views.logout,name="logout"),
    path('registration', views.reg, name="registration"),
    path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
    path('check_email_availability/', views.check_email_availability, name='check_email_availability'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  
    path('dashboard/',views.dashboard,name="dashboard"),  
    path('cart/',views.cart,name="cart"), 
    path('success/',views.success,name="success"), 
    path('backup/',views.backup,name="backup"), 
    path('userreg/',views.userreg,name="userreg"),
    path('profile_update/',views.profile_update,name="profile_update"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('doctors/',views.doctors,name="doctors"),
    path('doctorsone/',views.doctorsone,name="doctorsone"),
    path('doctorstwo/',views.doctorstwo,name="doctorstwo"),
    path('doctorsthree/',views.doctorsthree,name="doctorsthree"),  
    path('services/add/', views.add_service, name='add_service'),
    path('services/', views.service_list, name='service_list'),  
    path('newservice/', views.newservice, name='newservice'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staffs/', views.staffs, name='staffs'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('staff_index/', views.staff_index, name='staff_index'),
    path('staff_service/', views.staff_service, name='staff_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('newcart/',views.newcart,name="newcart"),
    path('acceptTerms/', views.acceptTerms, name="acceptTerms"),
   
    path('feedback_thankyou/', views.feedback_thankyou, name="feedback_thankyou"),
    path('adminfeedback/', views.adminfeedback, name="adminfeedback"),
    path('boarding_appointment/', views.boarding_appointment, name="boarding_appointment"),
    path('payment/<int:boarding_id>/',views.payment, name='payment'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('user_index/review/', review, name='review'),
    path('user_bookings/', user_bookings, name='user_bookings'),
    path('Vacc/', views.Vacc, name='Vacc'),
    path('alert/', views.alert, name='alert'),
    path('boardingapp/<int:boarding_id>/', views.boardingapp, name='boardingapp'),
    path('add_boarding/', views.add_boarding, name='add_boarding'),
    path('boarding_list/', views.boarding_list, name='boarding_list'),
    path('boarding_list1/', views.boarding_list1, name='boarding_list1'),
    path('delete/<int:boarding_id>/', views.delete_boarding, name='delete_boarding'),
    path('make_available/<int:boarding_id>/', views.make_available, name='make_available'),
    path('make_unavailable/<int:boarding_id>/', views.make_unavailable, name='make_unavailable'),
    path('boardingindex/', views.boardingindex, name='boardingindex'),
    # path('boarding/<int:boarding_id>/', views.boarding_detail, name='boarding_detail'),
    path('boarding/<int:boarding_id>/', views.boarding_detail, name='boarding_detail'),
    path('Petcare_services/', views.Petcare_services, name='Petcare_services'),
    path('send_verification_email/', send_verification_email, name='send_verification_email'),
    path('add_vaccination', views.add_vaccination, name='add_vaccination'),
    path('vaccination_list1/', views.vaccination_list1, name='vaccination_list1'),
    path('live_search/', views.live_search, name='live_search'),
    path('delete_vaccination/<int:vaccination_id>/', views.delete_vaccination, name='delete_vaccination'),
    path('vaccination_list/', views.vaccination_list, name='vaccination_list'),
    path('result/', views.result, name='image_result'),
    path('timer_clock/', views.timer_clock, name='timer_clock'),
    path('VaccDetails/', views.VaccDetails, name='VaccDetails'),
    path('confirmbooking/<int:boarding_id>/', views.confirmbooking, name='confirmbooking'),
    path('download_file/', views.download_file, name='download_file'),
    path('Staff_leave/', staff_leave_view, name='staff_leave'),
   
    path('leave-application/',views.leave_application, name='leave_application'),
    path('admin_leave_approval/', views.admin_leave_approval, name='admin_leave_approval'),
    path('leave_approval_action/', views.leave_approval_action, name='leave_approval_action'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
   
    
   
    ]
    
    
    
   
         
