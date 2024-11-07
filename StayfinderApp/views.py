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
    hotel_id= request.GET["hotel"]

    hotelDetails=Hotel.objects.filter(pk=hotel_id)[0]
    room_list=Room.objects.filter(hotel=hotel_id)

    context={
        "hotelDetails":hotelDetails,
        "room_list":room_list,       
        }
    return render(request, 'HotelDetails/hotelDetails.html',context)


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


