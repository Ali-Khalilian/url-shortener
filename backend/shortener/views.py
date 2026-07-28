from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from django.core.cache import cache

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

        # 1. Check Redis first
        cached_link = cache.get(short_code)

        if cached_link:

            Click.objects.create(
                link_id=cached_link["id"],
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )

            return redirect(cached_link["url"])

        # 2. Redis miss -> Get from database
        link = get_object_or_404(Link, short_code=short_code)

        # 3. Save link data in Redis
        cache.set(
            short_code, {"id": link.id, "url": link.original_url}, timeout=60 * 60
        )

        # 4. Save click analytics
        Click.objects.create(
            link=link,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )

        # 5. Redirect
        return redirect(link.original_url)
