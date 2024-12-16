from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login 
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from .models import AdsSlide, Hotel, Role, Room,UserRole
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
            print(email)
            print(password)
            if User.objects.filter(email=email).exists():
                user = authenticate(request, username=User.objects.get(email=email).username, password=password)
                print(user)
                if user is not None:
                    # login(user)
                    auth_login(request, user)
                    return redirect('/')
                else:
                    print("Wrong Credential")

            else:
                print("Wrong Credential")

        except Exception as e:
            print("error----"+str(e))


    
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
