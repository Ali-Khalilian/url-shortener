from django.urls import path
from .views import CreateLinkAPIView, RedirectLinkAPIView

urlpatterns = [
    path("shorten/", CreateLinkAPIView.as_view()),
    path("<str:short_code>/", RedirectLinkAPIView.as_view()),
]
