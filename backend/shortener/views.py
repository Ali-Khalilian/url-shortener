from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from .models import Link, Click
from .serializers import LinkSerializer
import random
import string


def generate_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


class CreateLinkAPIView(APIView):

    def post(self, request):

        url = request.data.get("url")

        code = generate_code()

        link = Link.objects.create(original_url=url, short_code=code)

        serializer = LinkSerializer(link)

        return Response(serializer.data)


class RedirectLinkAPIView(APIView):

    def get(self, request, short_code):

        link = get_object_or_404(Link, short_code=short_code)

        Click.objects.create(link=link, ip_address= request.META.get("REMOTE_ADDR"), user_agent=request.META.get("HTTP_USER_AGENT"))

        return redirect(link.original_url)
