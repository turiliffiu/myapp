from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Crea l'utente amministratore iniziale.
    Uso: python manage.py create_admin
    """
    help = 'Crea un utente amministratore predefinito'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'Admin123!'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Utente "{username}" già esiste.'))
            return

        user = User.objects.create_superuser(
            username=username,
            email='admin@myapp.local',
            password=password,
        )
        user.profile.role = 'admin'
        user.profile.save()

        self.stdout.write(self.style.SUCCESS(f'✅ Admin creato: {username} / {password}'))
        self.stdout.write(self.style.WARNING('⚠️  Cambia password dopo il primo login!'))
