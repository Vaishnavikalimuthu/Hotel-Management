from django.shortcuts import render,HttpResponse,redirect
from .models import *
from .forms import *
from django.views.generic import ListView,View,DeleteView
from django.urls import reverse, reverse_lazy
from app.booking_functions.get_random_person_name_email import get_random_person_name_email
from app.booking_functions.availability import check_availability

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content, Personalization
import environ

import stripe
stripe.api_key = 'sk_test_51Hu0AzH60lA1oSoomphzz4KWIOkf3fyNb6xKnMTLtZuqrYsafvJvMOQXhqxqOV0vy7EkWSuJxV3GxH5q899R8M8l00MDvjRsHl'

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env()

def home(request):
    return render(request,'app/home.html')

def every(request):
    return render(request,'app/every.html')

def gallery(request):
    return render(request,'app/gallery.html')

def awards(request):
    return render(request,'app/awards.html')

def contact(request):
    return render(request,'app/contact.html')

def carrer(request):
    return render(request,'app/carrers.html')

def branch1(request):
    return render(request,'app/branch1.html')

def branch2(request):
    return render(request,'app/branch2.html')

# def accom(request):
#     return render(request,'app/accomhtml')

def service(request):
    return render(request,'app/service.html')

def dinning(request):
    return render(request,'app/dinning.html')

def location(request):
    return render(request,'app/location.html')

def contactus(request):
    return render(request,'app/contactus.html')

def contactus1(request):
    return render(request,'app/contactus1.html')

def events(request):
    return render(request,'app/events.html')

def meeting(request):
    return render(request,'app/meeting.html')

def reserve(request):
    return render(request,'app/reserve.html')

def roomlist(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomDetailView', kwargs={'category': room_category})
        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
    }
    return render(request, 'app/room_list_view.html', context)

class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.request.user)
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
        print(room_list)
        print(category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'booking/room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]

            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            message = Mail(from_email=Email('vaishnavikalimuthu.2@@gmail.com'))
            message.add_content(Content('text/html', '<strong>Sending from hotelina</strong>'))
            message.subject = 'Sending from The Moonlight Resart'
            personalization = Personalization()
            personalization.add_to(Email('vaishnavikalimuthu.24@gmail.com'))
            message.add_personalization(personalization)
            try:
                sg = SendGridAPIClient(api_key=os.getenv('SG_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                print('SENT!!!')
                return HttpResponse("Booking confirmed and email sent!")
            except Exception as e:
                print(f"Error: {e}")
            return redirect('CheckoutView')

class BookingListView(ListView):
    model = Booking
    template_name = "booking/booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

def payment(request):
    return render(request,'booking/payment.html')

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking/booking_cancel_view.html'
    success_url = reverse_lazy('BookingListView')

class CheckoutView(View):

    def get(self, request, *args, **kwargs):
        person_form = PersonForm()
        context = {
            "person_form": person_form,
        }
        return render(request, 'booking/checkout.html', context)

    def post(self, request, *args, **kwargs):
        person_name, person_email = get_random_person_name_email()

        customer = stripe.Customer.create(
            name=person_name,
            email=person_email
        )
        person = Person.objects.create(
            name=person_name,
            email=person_email
        )
        person.save()
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
        
        stripe.api_key = 'sk_test_51Hu0AzH60lA1oSoomphzz4KWIOkf3fyNb6xKnMTLtZuqrYsafvJvMOQXhqxqOV0vy7EkWSuJxV3GxH5q899R8M8l00MDvjRsHl'
        request.session['amount'] = 15000
        
        if 'amount' in request.session:
            amount = request.session['amount']
        else:
            print("Amount not set in session.")
        
        amount_in_cents = int(request.session['amount']) * 100

        print(f"Amount for Stripe: {amount_in_cents}")

        room_category = request.session.get('room_category', 'Default Room Category') 
        if room_category == 'Default Room Category':
            print("Warning: Room category not set in session. Using default value.")
        
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        
        # request.session['check_in'] = data['check_in']
        # request.session['check_out'] = data['check_out']


        check_in = request.session.get('check_in', '2024-01-01')  # Default value
        check_out = request.session.get('check_out', '2024-01-02')  # Default value
        # Check if 'check_in' and 'check_out' are actually set
        # if check_in == '2024-01-01' or check_out == '2024-01-02':
        #     print("Warning: Check-in or Check-out not")
        
        checkout_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/success",
        cancel_url="http://127.0.0.1:8000/cancel",
        payment_method_types=["card"],
        line_items=[
            {
            'price_data': {
                'currency': 'inr',
                'unit_amount': amount_in_cents,
                'product_data': {
                'name': room_category,

                            },
                        },
                        'quantity': 1
                    },

                ],
                mode="payment",
            )
        print(request.session.get('amount', 'Amount not set in session'))

        context = {
                'person': person,
                'checkout_id': checkout_session.id,
                'amount': request.session['amount'],
                'room_image': '',
                'room_name': room_category,
                'amount': request.session['amount'],
                'check_in': check_in,
                'check_out':check_out,
            }
        print('chkout_context = ', context)
        return render(request, 'booking/checkout_confirm.html',context)


def success_view(request):
    return render(request, 'booking/success.html')


def cancel_view(request):
    return render(request, 'booking/cancel.html')    
        # 
        # try:
        #     stripe.api_key = 'sk_test_51Hu0AzH60lA1oSoomphzz4KWIOkf3fyNb6xKnMTLtZuqrYsafvJvMOQXhqxqOV0vy7EkWSuJxV3GxH5q899R8M8l00MDvjRsHl'
        #     checkout_session = stripe.checkout.Session.create(
        #         success_url="http://127.0.0.1:8000/success",
        #         cancel_url="http://127.0.0.1:8000/cancel",
        #         payment_method_types=["card"],
        #         line_items=[
        #             {
        #                 'price_data': {
        #                     'currency': 'inr',
        #                     'unit_amount': int(request.session['amount'])*100,
        #                     'product_data': {
        #                         'name': request.session['room_category'],

        #                     },
        #                 },
        #                 'quantity': 1
        #             },

        #         ],
        #         mode="payment",
        #     )

        #     context = {
        #         'person': person,
        #         'checkout_id': checkout_session.id,
        #         'amount': request.session['amount'],
        #         'room_image': '',
        #         'room_name': request.session['room_category'],
        #         'amount': request.session['amount'],
        #         'check_in': request.session['check_in'],
        #         'check_out': request.session['check_out'],
        #     }
        #     print('chkout_context = ', context)

        #     return render(request, 'booking/checkout_confirm.html',context)
        # except Exception as e:
        #     print('failed , ', request.session)
        #     return render(request, 'booking/failure.html', {'error': e})


# def contact_us(request):
#     return render(request, 'app/contact.html')

# class RoomDetailView(View):
#     def get(self, request, *args, **kwargs):
#         category = self.kwargs.get('category', None)
#         form = AvailabilityForm()
#         room_list = Room.objects.filter(category=category)
#         print(room_list)
#         print(category)
#         if len(room_list) > 0:
#             room = room_list[0]
#             room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
#             context = {
#                 'room_category': room_category,
#                 'form': form,
#             }
#             return render(request, 'booking/room_detail_view.html', context)
#         else:
#             return HttpResponse('Category does not exist')

#     def post(self, request, *args, **kwargs):
#         category = self.kwargs.get('category', None)
#         room_list = Room.objects.filter(category=category)
#         form = AvailabilityForm(request.POST)

#         if form.is_valid():
#             data = form.cleaned_data
#         available_rooms = []
#         for room in room_list:
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)

#         if len(available_rooms) > 0:
#             room = available_rooms[0]
#             booking = Booking.objects.create(
#                 user=self.request.user,
#                 room=room,
#                 check_in=data['check_in'],
#                 check_out=data['check_out']
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse('All of this category of rooms are booked!! Try another one')


# class BookingView(FormView):
#     form_class = AvailabilityForm
#     template_name = 'availability_form.html'

#     def form_valid(self, form):
#         data = form.cleaned_data
#         room_list = Room.objects.filter(category=data['room_category'])
#         available_rooms = []
#         for room in room_list:
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)

#         if len(available_rooms) > 0:
#             room = available_rooms[0]
#             booking = Booking.objects.create(
#                 user=self.request.user,
#                 room=room,
#                 check_in=data['check_in'],
#                 check_out=data['check_out']
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse('All of this category of rooms are booked!! Try another one')


# _________________first_______________________

# def check_booking(uid, room_count, start_date, end_date):
#     qs = HotelBooking.objects.filter(hotel__uid=uid)
#     # qs1 = qs.filter(
#     #     start_date__gte=start_date,
#     #     end_date__lte=end_date,
#     # )
#     # qs2 = qs.filter(
#     #     start_date__lte=start_date,
#     #     end_date__gte=end_date,
#     # )

#     qs = qs.filter(
#         Q(start_date__gte=start_date,
#           end_date__lte=end_date)
#         | Q(start_date__lte=start_date,
#             end_date__gte=end_date)
#     )
#     # qs = qs1|qs2

#     if len(qs) >= room_count:
#         return False
#     return True


# def index(request):
#     amenities = Amenities.objects.all()
#     hotels = Hotel.objects.all()
#     total_hotels = len(hotels)  
#     selected_amenities = request.GET.getlist('selectAmenity')
#     sort_by = request.GET.get('sortSelect')
#     search = request.GET.get('searchInput')
#     startdate = request.GET.get('startDate')
#     enddate = request.GET.get('endDate')
#     price = request.GET.get('price')

#     if selected_amenities != []:
#         hotels = hotels.filter(
#             amenities__amenity_name__in=selected_amenities).distinct()
#     if search:
#         hotels = hotels.filter(Q(hotel_name__icontains=search) | Q(description__icontains=search) | Q(amenities__amenity_name__contains=search))
        
#     if sort_by:
#         if sort_by == 'low_to_high':
#             hotels = hotels.order_by('hotel_price')
#         elif sort_by == 'high_to_low':
#             hotels = hotels.order_by('-hotel_price')
#     if price:
#         hotels = hotels.filter(hotel_price__lte=int(price))
#     if startdate and enddate:
#         unbooked_hotels = []
#         for i in hotels:
#             valid = check_booking(i.uid, i.room_count, startdate, enddate)
#             if valid:
#                 unbooked_hotels.append(i)
#         hotels = unbooked_hotels
#     hotels = hotels.distinct ()
#     p = Paginator(hotels, 2)
#     page_no = request.GET.get('page')
#     hotels = p.get_page(1)

#     if page_no:
#         hotels = p.get_page(page_no)
#     no_of_pages = list(range(1, p.num_pages+1))

#     date = datetime.today().strftime('%Y-%m-%d')

#     context = {'amenities': amenities, 'hotels': hotels, 'sort_by': sort_by,
#                'search': search, 'selected_amenities': selected_amenities, 'no_of_pages': no_of_pages, 'max_price': price, 'startdate': startdate, "enddate": enddate, "date": date,'total_hotels':total_hotels}
#     return render(request, 'home/index.html', context)


# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user_obj = authenticate(request, username=username, password=password)
#         if user_obj:
#             login(request, user_obj)
#             messages.success(request, 'Sigin Successfull')
#             return redirect('/')
#         else:
#             messages.error(request, 'Please Enter Valid Name Or Password.')
#             return redirect('/')

#     return render(request, 'home/signin.html')


# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']

#         user = User.objects.filter(username=username)
#         if not user.exists():
#             user = User.objects.create(
#                 username=username, password=password, email=email)
#             user.save()
#             messages.success(request, 'Welcome , Sigup Successfull')
#             return render(request, 'home/signin.html')
#         else:
#             messages.error(
#                 request, 'Username Or Email Already Exist Please Enter Diffrent Values.')
#             redirect('signin')
#     return render(request, 'home/signup.html')


# def signout(request):
#     logout(request)
#     return redirect('/')


# def get_hotel(request, uid):
#     hotel = Hotel.objects.get(uid=uid)
#     context = {'hotel': hotel}
#     context['date'] = datetime.today().strftime('%Y-%m-%d')
    
#     if request.method == 'POST':
#         checkin = request.POST.get('startDate')
#         checkout = request.POST.get('endDate')
#         context['startdate'] = checkin
#         context['enddate'] = checkout

#         try:
#             valid = check_booking(
#                 hotel.uid, hotel.room_count, checkin, checkout)
#             if not valid:
#                 messages.error(request, 'Booking for these days are full')
#                 return render(request, 'home/hotel.html', context)
#         except:
#             messages.error(request, 'Please Enter Valid Date Data')
#             return render(request, 'home/hotel.html', context)
#         HotelBooking.objects.create(hotel=hotel, user=request.user, start_date=checkin,
#                                     end_date=checkout, booking_type='Pre Paid')
#         messages.success(
#             request, f'{hotel.hotel_name} Booked successfully your booking id is {HotelBooking.uid}.')
#         return render(request, 'home/hotel.html', context)
#     return render(request, 'home/hotel.html', context)

# ---------------------Second

# ROOMS = [
#     {"id": 1, "number": "101", "room_type": "Deluxe", "price_per_night": 10200, "available": True},
#     {"id": 2, "number": "102", "room_type": "Club Room", "price_per_night": 11900, "available": True},
#     {"id": 3, "number": "103", "room_type": "Executive Suite", "price_per_night": 18275, "available": True},
# ]

# def available_rooms(request):
#     available_rooms = [room for room in ROOMS if room["available"]]
#     return render(request, 'app/available_rooms.html', {'rooms': available_rooms})

# def book_room(request, room_id):
#     room = next((room for room in ROOMS if room["id"] == room_id), None)
#     if not room:
#         return HttpResponse("Room not found", status=404)

#     if request.method == "POST":
#         guest_name = request.POST.get('guest_name')
#         check_in = request.POST.get('check_in')
#         check_out = request.POST.get('check_out')
        
#         booking = {
#             "guest_name": guest_name,
#             "check_in": check_in,
#             "check_out": check_out,
#             "room_id": room_id,
#             "room_number": room["number"],
#             "room_type": room["room_type"],
#             "price_per_night": room["price_per_night"]
#         }

#         if 'bookings' not in request.session:
#             request.session['bookings'] = []
#         request.session['bookings'].append(booking)
#         request.session.modified = True

#         # Mark the room as unavailable temporarily
#         room['available'] = False

#         return redirect('booking_confirmation', booking_id=len(request.session['bookings']) - 1)

#     return render(request, 'app/book_room.html', {'room': room})

# def booking_confirmation(request, booking_id):
#     bookings = request.session.get('bookings', [])
#     if booking_id < 0 or booking_id >= len(bookings):
#         return HttpResponse("Invalid booking ID", status=404)

#     booking = bookings[booking_id]
#     return render(request, 'app/booking_confirmation.html', {'booking': booking})

#-----------Third method

# def room_list(request):
#     rooms = Room.objects.all()
#     return render(request, 'booking/room_list.html', {'rooms': rooms})

# def party_hall_list(request):
#     party_halls = PartyHall.objects.all()
#     return render(request, 'booking/party_hall_list.html', {'party_halls': party_halls})

# def book_room_or_party_hall(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.save()
#             return redirect('payment', booking_id=booking.id)
#     else:
#         form = BookingForm()

#     return render(request, 'booking/book_room_or_party_hall.html', {'form': form})

# def payment(request, booking_id):
#     booking = Booking.objects.get(id=booking_id)
#     if request.method == 'POST':
#         booking.payment_status = True  # Mark the payment as completed
#         booking.save()
#         return redirect('confirmation', booking_id=booking.id)
#     return render(request, 'booking/payment.html', {'booking': booking})

# def booking_confirmation(request, booking_id):
#     booking = Booking.objects.get(id=booking_id)
#     return render(request, 'booking/booking_confirmation.html', {'booking': booking})

