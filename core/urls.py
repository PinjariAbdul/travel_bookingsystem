from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home_view, name='home'),  # homepage
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('explore/', views.travel_list_view, name='travel_list'),
    path('book/<int:travel_id>/', views.book_travel_view, name='book_travel'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail_view, name='booking_detail'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
]
