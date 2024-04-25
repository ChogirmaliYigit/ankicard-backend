from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomToken, User, Word
from users.serializers import UserSerializer, WordDetailSerializer, WordListSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        user = User.objects.filter(
            username=request.data["username"], password=request.data["password"]
        ).first()
        if user:
            token, created = CustomToken.objects.get_or_create(
                user=user,
                expires_at=timezone.now()
                + timedelta(days=settings.DEFAULT_TOKEN_EXPIRE_DAYS),
            )
            return Response(
                {"token": token.key, "user": UserSerializer(instance=user).data}
            )
        else:
            return Response({"error": "Username or password is invalid"}, status=401)


class WordListView(APIView):
    serializer_class = WordListSerializer

    def get_queryset(self, request):
        queryset = request.user.words.all()
        is_favorite = request.query_params.get("is_favorite", None)
        start_date = request.query_params.get(
            "start_date", date.today() - relativedelta(months=6)
        )
        end_date = request.query_params.get("end_date", date.today())
        if start_date:
            queryset = queryset.filter(
                created_at__date__gte=start_date, created_at__date__lte=end_date
            )
        if is_favorite:
            queryset = queryset.filter(is_favorite=is_favorite == "true")
        return queryset

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(request), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status.HTTP_201_CREATED)


class WordDetailView(APIView):
    serializer_class = WordDetailSerializer

    def get(self, request, pk):
        word = get_object_or_404(Word, pk=pk, user=request.user)
        serializer = self.serializer_class(instance=word)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        word = get_object_or_404(Word, pk=pk, user=request.user)
        serializer = self.serializer_class(instance=word, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status.HTTP_200_OK)

    def delete(self, request, pk):
        word = get_object_or_404(Word, pk=pk, user=request.user)
        word.delete()
        return Response({}, status.HTTP_204_NO_CONTENT)
