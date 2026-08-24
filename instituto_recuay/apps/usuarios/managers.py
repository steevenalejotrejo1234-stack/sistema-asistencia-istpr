from django.contrib.auth.models import UserManager


class UsuarioManager(UserManager):
    def get_by_dni(self, dni):
        return self.get(dni=dni)
