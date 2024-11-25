from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.

# class RoomCategory(models.Model):
#     category = models.CharField(max_length=50)
#     rate = models.FloatField()

#     def __str__(self):
#         return self.category


class Room(models.Model):
    ROOM_CATEGORIES = (
        ('DE', 'DELUXE'),
        ('CL', 'CLUB ROOM'),
        ('EX', 'EXECUTIVE SUITE'),
        ('PR', 'PRESIDENTAL '),
        ('AP', 'Apartment'),
    )
    number = models.IntegerField()
    beds = models.IntegerField()
    capacity = models.IntegerField()
    category = models.CharField(max_length=50,choices=ROOM_CATEGORIES)
    rate = models.FloatField()
    def __str__(self):
        return f'{self.number}. Beds = {self.beds} People = {self.capacity}'


class Booking(models.Model):
    PAYMENT_STATUSES = (
        ('COM', 'PAYMENT_COMPLETE'),
        ('INC', 'PAYMENT_INCOMPLETE'),
        ('PAR', 'PAYMENT_PARTIALLY_COMPLETE'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    payment_status = models.CharField(max_length=3, choices=PAYMENT_STATUSES)

    def __str__(self):
        return f'From = {self.check_in.strftime("%d-%b-%Y %H:%M")} To = {self.check_out.strftime("%d-%b-%Y %H:%M")}'

    def get_cancel_booking_url(self):
        return reverse_lazy('hotel:CancelBookingView', args=[self.pk, ])

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

# import uuid

# class Room(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     capacity = models.IntegerField()
#     price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.name

# class PartyHall(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     capacity = models.IntegerField()
#     price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.name

# class Booking(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
#     party_hall = models.ForeignKey(PartyHall, on_delete=models.CASCADE, null=True, blank=True)
#     customer_name = models.CharField(max_length=100)
#     customer_email = models.EmailField()
#     booking_date = models.DateTimeField(default=timezone.now)
#     duration_in_hours = models.IntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_status = models.BooleanField(default=False)  # Payment status: False = Pending, True = Paid

#     def save(self, *args, **kwargs):
#         if self.room:
#             self.total_price = self.room.price_per_hour * self.duration_in_hours
#         elif self.party_hall:
#             self.total_price = self.party_hall.price_per_day
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Booking for {self.customer_name}"


# class BaseModel(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now_add=True)

#     class Meta:
#         abstract = True
#         ordering=['uid']


# class Amenities:
#     amenity_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.amenity_name

# class Hotel:
#     hotel_name= models.CharField(max_length=100)
#     hotel_price = models.IntegerField()
#     description = models.TextField()
#     # amenities = models.ManyToManyField(Amenities)
#     room_count = models.IntegerField(default=10)

#     def __str__(self) :
#         return self.hotel_name

# class HotelImages:
#     hotel= models.ForeignKey(Hotel ,related_name="images", on_delete=models.CASCADE)
#     images = models.ImageField(upload_to="hotels")


# class HotelBooking:
#     hotel= models.ForeignKey(Hotel  , related_name="hotel_bookings" , on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name="user_bookings" , on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     booking_type= models.CharField(max_length=100,choices=(('Pre Paid' , 'Pre Paid') , ('Post Paid' , 'Post Paid')))
    
#     def __str__(self):
#         return f'{self.hotel.hotel_name} {self.start_date} to {self.end_date}'