import re
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_yasg import openapi, utils
from rest_framework import generics, permissions, status, validators
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Word
from users.serializers import UserSerializer, WordDetailSerializer, WordListSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @utils.swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD
                ),
            },
        ),
        responses={
            status.HTTP_201_CREATED: UserSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
    )
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if not user:
            raise validators.ValidationError("Username or password is invalid")
        return Response(UserSerializer(instance=user).data, status.HTTP_200_OK)


class WordListView(APIView):
    serializer_class = WordListSerializer

    def get_queryset(self, request):
        queryset = request.user.words.all()
        is_favorite = request.query_params.get("is_favorite", None)
        start_date = request.query_params.get(
            "start_date", date.today() - relativedelta(months=6)
        )
        end_date = request.query_params.get("end_date", date.today())

        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, str(start_date)):
            raise validators.ValidationError(
                {
                    "start_date": f"'{start_date}' value has an invalid date format. It must be in YYYY-MM-DD format."
                }
            )

        if not re.match(date_pattern, str(end_date)):
            raise validators.ValidationError(
                {
                    "end_date": f"'{end_date}' value has an invalid date format. It must be in YYYY-MM-DD format."
                }
            )

        try:
            queryset = queryset.filter(
                created_at__date__gte=start_date, created_at__date__lte=end_date
            )
        except ValidationError as e:
            raise validators.ValidationError(e.message % e.params)

        if is_favorite:
            queryset = queryset.filter(is_favorite=is_favorite == "true")

        return queryset

    @utils.swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Start date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="End date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "is_favorite",
                openapi.IN_QUERY,
                description="Is Favorite",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={
            status.HTTP_200_OK: WordListSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
    )
    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(request), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @utils.swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["front", "back", "pronunciation"],
            properties={
                "front": openapi.Schema(type=openapi.TYPE_STRING),
                "back": openapi.Schema(type=openapi.TYPE_STRING),
                "pronunciation": openapi.Schema(type=openapi.TYPE_STRING),
                "is_favorite": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={
            status.HTTP_201_CREATED: "{}",
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status.HTTP_201_CREATED)


class WordDetailView(APIView):
    serializer_class = WordDetailSerializer

    @utils.swagger_auto_schema(
        responses={
            status.HTTP_200_OK: WordDetailSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
    )
    def get(self, request, pk):
        word = get_object_or_404(Word, pk=pk, user=request.user)
        serializer = self.serializer_class(instance=word)
        return Response(serializer.data, status.HTTP_200_OK)

    @utils.swagger_auto_schema(
        responses={
            status.HTTP_200_OK: "{}",
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
    )
    def put(self, request, pk):
        word = get_object_or_404(Word, pk=pk, user=request.user)
        serializer = self.serializer_class(instance=word, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status.HTTP_200_OK)

    @utils.swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "{}",
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
    )
    def delete(self, request, pk):
        word = get_object_or_404(Word, pk=pk, user=request.user)
        word.delete()
        return Response({}, status.HTTP_204_NO_CONTENT)
