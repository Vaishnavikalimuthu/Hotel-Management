import random
from django.conf import settings

def get_random_person_name_email():
    file_path = settings.BASE_DIR / "app" / "booking_functions" / "text_lists" / "names.txt"
    with open(file_path, "r") as f:
        tlds = ['.com', '.net', '.co.uk', '.edu', '.tech', '.dev']
        data = f.read().lower().split(',')
        names = list(map(str.strip, data))
        name = random.choice(names)
        mail_domain = random.choice(names)
        tld = random.choice(tlds)
        separator = '@'
        email = name + separator + mail_domain + tld

        return(name, email)