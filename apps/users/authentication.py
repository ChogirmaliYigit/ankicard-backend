from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import CustomToken


class CustomTokenAuthentication(TokenAuthentication):
    # List of endpoints that do not require authentication
    allowed_endpoints = [
        "/swagger/",
        "/admin/",
    ]

    def authenticate(self, request):
        if any(
            request.path.startswith(endpoint) for endpoint in self.allowed_endpoints
        ):
            return None  # No authentication required

        try:
            key = request.headers.get("Authorization", "").split()[-1]
            token = CustomToken.objects.filter(key=key).first()
        except IndexError:
            token = None

        if not token:
            raise AuthenticationFailed("Token not provided")
        elif token and token.expires_at < timezone.now():
            raise AuthenticationFailed("Token")

        return token.user, token
