import datetime
from app.models import Room

def find_total_room_charge(check_in, check_out, category):
    days = check_out-check_in
    room_category = Room.objects.get(category=category)
    total = days.days * room_category.rate
    return total