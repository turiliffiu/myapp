from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Popola il database con utenti di esempio.
    Uso: python manage.py seed_db
    """
    help = 'Seed del database con dati di esempio'

    USERS = [
        {'username': 'admin',   'password': 'Admin123!',  'role': 'admin',  'email': 'admin@myapp.local',   'first_name': 'Admin',  'last_name': 'User'},
        {'username': 'editor1', 'password': 'Editor123!', 'role': 'editor', 'email': 'editor@myapp.local',  'first_name': 'Mario',  'last_name': 'Rossi'},
        {'username': 'viewer1', 'password': 'Viewer123!', 'role': 'viewer', 'email': 'viewer@myapp.local',  'first_name': 'Giulia', 'last_name': 'Bianchi'},
    ]

    def handle(self, *args, **options):
        for data in self.USERS:
            if User.objects.filter(username=data['username']).exists():
                self.stdout.write(f'  ℹ️  {data["username"]} — già presente')
                continue

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            user.profile.role = data['role']
            user.profile.save()

            if data['role'] == 'admin':
                user.is_superuser = True
                user.is_staff = True
                user.save()

            self.stdout.write(self.style.SUCCESS(f'  ✅ {data["username"]} ({data["role"]})'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Seed completato!'))
