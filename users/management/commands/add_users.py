from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone


class Command(BaseCommand):
    help = 'Load data from custom user list'


    user_credentials = [
        {
            "username": "sarah.johnson",
            "email": "sarahj@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "verified.account",
            "email": "verifiedaccount@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "kenyan.coolkid",
            "email": "kenyancoolkid@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "van.guard",
            "email": "vanguard@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "amanda.jepson",
            "email": "amandajp@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "code.wizard",
            "email": "codewizard@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "thee.coder.girl",
            "email": "codergirl@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "brenda.jones",
            "email": "bjones@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
        {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "phone_no": "+254112345678",
            "password": "morikeli",
        },
    ]


    def handle(self, *args, **kwargs):
        current_dt = timezone.datetime.now()    # current datetime

        for user_data in self.user_credentials:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']

            try:
                user = get_user_model().objects.create_user(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
            
            except IntegrityError:    # if the user credentials exists, print the message below.
                self.stdout.write(self.style.ERROR(f'User account with credentials {email} or {username} exists!'))
                continue    # continue saving other user credentials.
        
        total_accounts = get_user_model().objects.filter(date_joined__date__gte=current_dt).count()
        self.stdout.write(self.style.HTTP_INFO(f'Total user accounts created (today): {total_accounts}'))