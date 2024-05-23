from django.db import transaction
from rest_framework import serializers
from users.models import User, Word


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def create(self, validated_data):
        user = User.objects.create_user(
            full_name=validated_data.get("full_name"),
            username=validated_data.get("username"),
            password=validated_data.get("password"),
            is_active=True,
            is_staff=False,
        )
        return user

    def get_token(self, user):
        return user.auth_token.key

    class Meta:
        model = User
        fields = ("username", "full_name", "password", "token")


class WordDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    front = serializers.CharField(required=False)
    back = serializers.CharField(required=False)
    pronunciation = serializers.CharField(required=False)
    is_favorite = serializers.BooleanField(required=False)

    class Meta:
        model = Word
        fields = (
            "id",
            "front",
            "back",
            "pronunciation",
            "is_favorite",
        )


class WordListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "front": instance.front,
            "back": instance.back,
            "pronunciation": instance.pronunciation,
            "is_favorite": instance.is_favorite,
        }

    def create(self, validated_data):
        request = self.context.get("request")
        words_data = validated_data.pop("words")
        word_objects = []
        for item in words_data:
            word_objects.append(
                Word(
                    front=item["front"],
                    back=item["back"],
                    pronunciation=item.get("pronunciation", ""),
                    is_favorite=item.get("is_favorite", False),
                    user=request.user,
                )
            )

        with transaction.atomic():
            created_words = []
            for word in word_objects:
                obj, created = Word.objects.get_or_create(
                    front=word.front,
                    back=word.back,
                    pronunciation=word.pronunciation,
                    user=word.user,
                    defaults={"is_favorite": word.is_favorite},
                )
                if not created:
                    obj.is_favorite = word.is_favorite
                    obj.save()
                created_words.append(obj)

        return created_words

    class Meta:
        model = Word
        fields = (
            "id",
            "front",
            "back",
            "pronunciation",
            "is_favorite",
        )
