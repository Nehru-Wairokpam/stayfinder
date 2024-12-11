from django.shortcuts import render

from .models import AdsSlide, Hotel, Room
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
    # Use .get() for safe access to query parameters
    hotel_id = request.GET.get("hotel")
    price = request.GET.get("price")
    capacity = request.GET.get("capacity", "1")  # Adding capacity as part of the filtering logic

    # Use .first() to fetch a single object or None, avoiding potential index errors
    hotelDetails = Hotel.objects.filter(pk=hotel_id).first()

    # Initialize room_list with the basic filter for the hotel
    room_list = Room.objects.filter(hotel=hotelDetails)
    is_filter = False  # To track if filters were applied

    # Apply price filter if provided
    if price:
        try:
            price = float(price)  # Convert to float if price is a numeric field
            room_list = room_list.filter(price__lte=price)
            is_filter = True
        except ValueError:
            pass  # Ignore invalid price input

    # Apply capacity filter if provided
    if capacity:
        try:
            capacity = int(capacity)  # Convert to integer for capacity filtering
            room_list = room_list.filter(capacity=capacity)
            is_filter = True
        except ValueError:
            pass  # Ignore invalid capacity input

    # Prepare context for rendering
    context = {
        "hotelDetails": hotelDetails,
        "room_list": room_list,
        "is_filter": is_filter,
        "price": price if price else "",  # Ensure the form can show the selected price
        "capacity": capacity if capacity else "1",  # Ensure the form can show the selected capacity
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


