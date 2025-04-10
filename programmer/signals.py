from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order, CategorySubscription, AuthorSubscription
from .utils import send_telegram_notification
from Birja.settings import TELEGRAM_BOT_TOKEN, USER_ID


@receiver(post_save, sender=Order)
def notify_subscribers_on_new_order(sender, instance, created, **kwargs):
    message = (f"Новый заказ: {instance.title}\n"
               f"Описание: {instance.full_description}\n"
               f"Цена: {instance.price} MDL\n"
               f"Дедлайн: {instance.deadline}")
    send_telegram_notification(message, USER_ID, TELEGRAM_BOT_TOKEN)
