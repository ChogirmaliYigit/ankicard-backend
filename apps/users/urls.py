from django.urls import path
from users.views import (
    UserLoginView,
    UserRegistrationView,
    WordDetailView,
    WordListView,
)

urlpatterns = [
    path("sign-up", UserRegistrationView.as_view(), name="sign-up"),
    path("sign-in", UserLoginView.as_view(), name="sign-in"),
    path("words", WordListView.as_view(), name="words-list"),
    path("word/<int:pk>", WordDetailView.as_view(), name="word-detail"),
]
