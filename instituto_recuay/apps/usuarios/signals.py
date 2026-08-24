from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.utils import OperationalError


@receiver(post_migrate)
def crear_superadmin(sender, **kwargs):
    if sender.name == 'apps.usuarios':
        try:
            Usuario = sender.get_model('Usuario')
            if not Usuario.objects.filter(username='pieroat05').exists():
                Usuario.objects.create_superuser(
                    username='pieroat05',
                    email='pieroat05@instituto-recuay.edu.pe',
                    password='SuperAdmin2026!',
                    first_name='Piero',
                    last_name='Administrador',
                    dni='00000001',
                    rol='super_admin',
                )
        except OperationalError:
            pass
