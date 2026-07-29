from celery import shared_task
from django.utils import timezone

from .models import Click


@shared_task
def save_click(link_id, ip_address, user_agent):

    Click.objects.create(
        link_id=link_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return "Click saved"


@shared_task
def daily_click_report():

    today = timezone.now().date()

    clicks = Click.objects.filter(
        created_at__date=today
    ).count()

    print(
        f"Today's clicks: {clicks}"
    )

    return clicks