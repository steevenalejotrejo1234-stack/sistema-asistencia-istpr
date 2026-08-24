from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea el Super Administrador del sistema'

    def handle(self, *args, **options):
        Usuario = get_user_model()
        username = 'pieroat05'
        email = 'pieroat05@instituto-recuay.edu.pe'
        password = 'SuperAdmin2026!'
        first_name = 'Piero'
        last_name = 'Administrador'
        dni = '00000001'

        if Usuario.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username}" ya existe. Omitiendo creacion.')
            )
            return

        user = Usuario.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            dni=dni,
            rol='super_admin',
            telefono='999999999',
            sexo='M',
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Super Administrador creado exitosamente!\n'
                f'  Usuario: {username}\n'
                f'  Contrasena: {password}\n'
                f'  Email: {email}\n'
                f'  DNI: {dni}\n'
                f'  Nombre: {first_name} {last_name}\n'
                f'\nIMPORTANTE: Cambie la contrasena despues de iniciar sesion por primera vez.'
            )
        )
