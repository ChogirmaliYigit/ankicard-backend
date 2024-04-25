from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import CustomToken


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        key = request.headers.get("Authorization", "").split()[-1]
        token = CustomToken.objects.filter(
            key=key,
            expires_at__gte=timezone.now(),
        ).first()

        if not token:
            raise AuthenticationFailed("Token has been expired")

        return token.user, token
