from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users.models import User, Word


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def to_representation(self, instance):
        token, created = Token.objects.get_or_create(user=instance)
        return {"token": token.key, "user": instance}

    class Meta:
        model = User
        fields = ("username", "full_name", "password")


class WordListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get("request")
        word = Word.objects.create(
            front=validated_data.get("front"),
            back=validated_data.get("back"),
            pronunciation=validated_data.get("pronunciation"),
            is_favorite=validated_data.get("is_favorite", False),
            user=request.user,
        )
        return word

    class Meta:
        model = Word
        fields = ("front", "back", "pronunciation", "is_favorite",)


class WordDetailSerializer(serializers.ModelSerializer):
    front = serializers.CharField(required=False)
    back = serializers.CharField(required=False)
    pronunciation = serializers.CharField(required=False)
    is_favorite = serializers.BooleanField(required=False)

    class Meta:
        model = Word
        fields = ("front", "back", "pronunciation", "is_favorite",)
