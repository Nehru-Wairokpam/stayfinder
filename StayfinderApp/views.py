from profile import Profile
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout 
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import AdsSlide, Hotel, Role, Room, UserRole, Booked,Payment
# Create your views here.

def home(request):
    ads_list = AdsSlide.objects.all()
    picked_hotel_list = Hotel.objects.all().filter(picked_of_day=True)
    top_ten_room_list = Room.objects.all().filter(top_ten=True)

    context={
        "ads_list":ads_list,
        "picked_hotel_list":picked_hotel_list,
        "top_ten_room_list":top_ten_room_list,
     
    }
    return render(request, 'Home/home.html',context)


def hotel(request):
    hotel_list = Hotel.objects.all()

    context={
        "hotel_list":hotel_list
    }
    return render(request, 'Home/hotel.html', context)



def pickedoftheday(request):
    picked_hotel_list = Hotel.objects.all().filter(picked_of_day=True)
     
    context={
        "picked_hotel_list":picked_hotel_list,
    }
    return render(request, 'Home/pickedoftheday.html',context)



def topTenRoomList(request):
    top_ten_room_list = Room.objects.all().filter(top_ten=True)
     
    context={
        "top_ten_room_list":top_ten_room_list,
    }
    return render(request, 'Home/topTenRoomList.html',context)


def hotel_Details(request):
    # Fetch query parameters
    hotel_id = request.GET.get("hotel")
    price = request.GET.get("price")
    capacity = request.GET.get("capacity")

    # Retrieve the hotel details safely
    hotelDetails = Hotel.objects.filter(pk=hotel_id).first()

    # Initialize the room list with all rooms for the selected hotel
    room_list = Room.objects.filter(hotel=hotelDetails)
    is_filter = False  # Track if any filter was applied

    # Apply price filter if provided
    if price:
        try:
            price = float(price)  # Ensure `price` is a float for numeric comparison
            room_list = room_list.filter(price__lte=price)
            is_filter = True
        except ValueError:
            price = None  # Reset to None if invalid input is provided

    # Apply capacity filter if provided
    if capacity:
        try:
            capacity = int(capacity)  # Ensure `capacity` is an integer
            room_list = room_list.filter(capacity=capacity)
            is_filter = True
        except ValueError:
            capacity = None  # Reset to None if invalid input is provided

    # Prepare context for rendering
    context = {
        "hotelDetails": hotelDetails,
        "room_list": room_list,
        "is_filter": is_filter,  # Indicate if any filters are active
        "price": price if price is not None else "",  # Pass the selected price for form pre-fill
        "capacity": capacity if capacity is not None else "",  # Pass the selected capacity for form pre-fill
    }

    return render(request, 'HotelDetails/hotelDetails.html', context)





def room_Details(request):
    room_id = request.GET["room"]
    room_List = Room.objects.filter(pk=room_id)[0]

    context={
        "room_List":room_List

    }
    return render(request, 'HotelDetails/roomDetails.html', context)

def search(request):
    if request.method == 'POST':
        searchHotel = request.POST.get("searchHotel_query")

        hotel_list = Hotel.objects.filter(hotel_name__icontains=searchHotel)

        context = {
            "hotel_list":hotel_list
            # "is_search":True
        }

        return render(request, 'Home/hotel.html', context)
    else:
        context = {
            "error":"Invalid Request"
        }
        return render(request, 'Home/hotel.html', context)

def login(request):
        return render(request, 'Home/login.html')

    
    
def login_post(request):
     if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            # print(email)
            # print(password)
            if User.objects.filter(email=email).exists():
                user = authenticate(request, username=User.objects.get(email=email).username, password=password)
                print(user)
                if user is not None:
                    # login(user)
                    auth_login(request, user)
                    return redirect('/')
                else:
                    context={
                        "status":"Error"
                    }
                    return render(request, 'Home/login.html')
                    

            else:
                context={
                        "status":"Error"
                    }
                return render(request, 'Home/login.html', context)

        except Exception as e:
            context={
                        "status":"Error"
                    }
            return render(request, 'Home/login.html',context)


    
def signUp(request):
        roles=Role.objects.all()

        context={
            "roles":roles
      
        }
        return render(request, 'Home/signUp.html',context)


def signup_post(request):
    if request.method == 'POST':
        full_name = request.POST['fullName']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        phone = request.POST['phone']
        address = request.POST['address']
        role = request.POST['role'] #id

        user = User.objects.create_user(username=full_name,email=email,password=password)
        if role == '1':
            user_role=UserRole.objects.create(user=user,role_id=int(role),user_name=full_name, phone=phone,address=address, is_activate=True)
        if role == '2':
            user_role=UserRole.objects.create(user=user,role_id=int(role),user_name=full_name, phone=phone,address=address, is_activate=False)


        context = {
         
        }
        
        return redirect('/login')
    else:
        context = {
            "error": "Invalid Request"
        }
        return redirect('/signUp')


    
def Logout(request):
        logout(request)
        return redirect('/')

@login_required
def profile_view(request):
    # Get or create profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    roles = Role.objects.all()  # Assuming you have a Role model

    # Pass profile data to the template
    return render(request, 'profile.html', {'profile': profile, 'roles': roles})


from datetime import datetime
date_format = "%Y-%m-%d"

@login_required
def Booking(request):
    room_id = request.GET.get("room_id")  # Get room ID from the URL or form
    hotel_id = request.GET.get("hotel")  # Get hotel ID for hotel details
    is_booked = False
    start_date, end_date, number_of_days = None, None, None

    # Fetch hotel details if hotel_id is provided
    hotelDetails = get_object_or_404(Hotel, pk=hotel_id) if hotel_id else None

    # Check if the room is already booked
    if room_id:
        booked_room = Booked.objects.filter(room_id=room_id).first()
        if booked_room:
            is_booked = True
            start_date = booked_room.start_date
            end_date = booked_room.end_date
            number_of_days = booked_room.number_of_days
        else:
            is_booked = False

    # Handle POST request
    if request.method == 'POST':
        try:
            # Extract POST data
            room_id = request.POST.get('room_id')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Ensure required fields are provided
            if not room_id or not start_date or not end_date:
                raise ValueError("All fields are required.")

            # Parse dates and calculate the number of days
            date_format = "%Y-%m-%d"
            start_date_obj = datetime.strptime(start_date, date_format)
            end_date_obj = datetime.strptime(end_date, date_format)

            if start_date_obj >= end_date_obj:
                raise ValueError("End date must be after start date.")

            n_o_d = end_date_obj - start_date_obj
            number_of_days = n_o_d.days + 1  # Include the end date

            # Convert dates to datetime format for database
            s_d = start_date_obj.strftime("%Y-%m-%d 12:00:00+00:00")
            e_d = end_date_obj.strftime("%Y-%m-%d 12:00:00+00:00")

            # Get user role and payment details
            user_role = UserRole.objects.get(user=request.user)
            payment = Payment.objects.first()  # Assuming the first payment record is used

            # Create booking
            Booked.objects.create(
                number_of_days=number_of_days,
                start_date=s_d,
                end_date=e_d,
                user_role=user_role,
                room_id=room_id,
                payment=payment
            )
            is_booked = True

            # Add a success message
            messages.success(request, "Room booked successfully!")
            # Redirect on success
            return redirect('/')

        except ValueError as e:
            # Handle validation errors
            context = {
                "hotelDetails": hotelDetails,
                "is_booked": is_booked,
                "start_date": start_date,
                "end_date": end_date,
                "number_of_days": number_of_days,
                "error": str(e),
            }
            return render(request, "HotelDetails/roomDetails.html", context)

        except Exception as e:
            # Handle unexpected errors
            context = {
                "hotelDetails": hotelDetails,
                "is_booked": is_booked,
                "start_date": start_date,
                "end_date": end_date,
                "number_of_days": number_of_days,
                "error": "An unexpected error occurred. Please try again.",
            }
            return render(request, "HotelDetails/roomDetails.html", context)

    # Render the booking page for GET requests
    context = {
        "hotelDetails": hotelDetails,
        "is_booked": is_booked,
        "start_date": start_date,
        "end_date": end_date,
        "number_of_days": number_of_days,
    }
    return render(request, "", context)