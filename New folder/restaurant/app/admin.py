from django.contrib import admin
from .models import *
# # Register your models here.
admin.site.register(Room)
# # admin.site.register(PartyHall)
admin.site.register(Booking)
# admin.site.register(RoomCategory)
admin.site.register(Person)

# admin.site.register((Hotel,HotelBooking,Amenities,HotelImages))
