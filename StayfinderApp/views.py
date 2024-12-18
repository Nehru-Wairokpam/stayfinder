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
        "top_ten_room_list":top_ten_room_list
    }
    return render(request, 'home.html',context)



def hotels(request):
    
    hotel_lists = Hotel.objects.all()

    context = {
        "hotel_lists":hotel_lists
    }

    
    return render(request, 'hotels.html', context)



def hotel_details(request):

    hotel_id= request.GET["hotel"]
    hotel_details=Hotel.objects.filter(pk=hotel_id)[0]
    room_list=Room.objects.filter(hotel=hotel_details)
    is_filter =False
    price=0
    capacity=1
    

    try: 
        price= request.GET["price"]
        room_list=Room.objects.filter(hotel=hotel_details, price__lt=price)
        is_filter=True
        price=price
    except:
        pass

    try: 
        capacity= request.GET["capacity"]
        room_list=Room.objects.filter(hotel=hotel_details, capacity=int(capacity))
        is_filter=True
        capacity=capacity

    except:
        pass

    context={
        "hotel_details":hotel_details,
        "room_list":room_list,
        'is_filter':is_filter,
        'price':price,
        'capacity':capacity


        
        }
    return render(request, 'hotel_details.html',context)




def room_details(request):
    room_id= request.GET["room"]
    room_details=Room.objects.filter(pk=room_id)[0]

    context={
        "room_details":room_details,
     
        }
    return render(request, 'room_details.html',context)


def search(request):

    if request.method == 'POST':
        query= request.POST.get("search_query")

    
        hotel_lists = Hotel.objects.filter(hotel_name__icontains=query)

        context = {
            "hotel_lists":hotel_lists,
            "is_search":True
        }

    
        return render(request, 'hotels.html', context)
    else:
        context = {
            "error":"Invalid Reequest"
        }
        return render(request, 'hotels.html', context)




