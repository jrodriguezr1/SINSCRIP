from django.contrib.auth.backends import ModelBackend
from inscrip.models import Estudian

class EstudianBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Estudian.objects.get(username=username)
        except Estudian.DoesNotExist:
            print('inscrip: Pasa al except, no hay ese user y por eso devuelve none')
            return None

        if user.check_password(password):
            print('inscrip: Simon, adelante man')

            return user
        return None