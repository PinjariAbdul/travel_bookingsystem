from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .forms import RegisterForm, ProfileUpdateForm, BookingForm
from .models import TravelOption, Booking
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login

def home_view(request):
    travels = TravelOption.objects.none()  # Show no data initially

    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    if travel_type or source or destination or date:
        travels = TravelOption.objects.all()
        if travel_type:
            travels = travels.filter(type=travel_type)
        if source:
            travels = travels.filter(source__icontains=source)
        if destination:
            travels = travels.filter(destination__icontains=destination)
        if date:
            travels = travels.filter(date_time__date=date)

    context = {
        'travels': travels,
        'selected_type': travel_type or '',
        'selected_source': source or '',
        'selected_destination': destination or '',
        'selected_date': date or '',
    }
    return render(request, 'home.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Authenticate and login user
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registered successfully. You are now logged in.")
                return redirect('home')  # or another page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    error_msg = None

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect on successful login
        else:
            # You can customize the message or use form.non_field_errors
            error_msg = "Invalid username or password or user not registered."

    return render(request, 'login.html', {'form': form, 'error_msg': error_msg})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('home')
    return render(request, 'logout_confirm.html')  # optional confirmation


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


def travel_list_view(request):
    travels = TravelOption.objects.all()
    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    if travel_type:
        travels = travels.filter(type=travel_type)
    if source:
        travels = travels.filter(source__icontains=source)
    if destination:
        travels = travels.filter(destination__icontains=destination)
    if date:
        travels = travels.filter(date_time__date=date)

    return render(request, 'travel_list.html', {'travels': travels})


@login_required
def book_travel_view(request, travel_id):
    travel = get_object_or_404(TravelOption, travel_id=travel_id)
    if travel.available_seats < 1:
        messages.error(request, "No seats available for this travel option.")
        return redirect('home')

    if request.method == 'POST':
        form = BookingForm(request.POST, max_seats=travel.available_seats)
        if form.is_valid():
            seats = form.cleaned_data['seats']
            total_price = seats * travel.price
            Booking.objects.create(
                user=request.user,
                travel_option=travel,
                number_of_seats=seats,
                total_price=total_price,
                booking_date=timezone.now(),
                status='Confirmed'
            )
            # Update available seats
            travel.available_seats -= seats
            travel.save()
            messages.success(request, f"Booking confirmed for {seats} seat(s).")
            return redirect('my_bookings')
    else:
        form = BookingForm(max_seats=travel.available_seats)

    return render(request, 'book_travel.html', {'travel': travel, 'form': form})


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if request.method == 'POST' and booking.status == 'Confirmed':
        booking.status = 'Cancelled'
        booking.save()
        # Release seats back to TravelOption
        travel = booking.travel_option
        travel.available_seats += booking.number_of_seats
        travel.save()
        messages.success(request, 'Booking cancelled successfully.')
    return redirect('my_bookings')


@login_required
def booking_detail_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'booking_details.html', {'booking': booking})
