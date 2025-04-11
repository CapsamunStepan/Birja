from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, CategorySubscription
from .utils import send_telegram_notification
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


@receiver(post_save, sender=Order)
def notify_subscribers_on_new_order(sender, instance, created, **kwargs):
    if created:
        category_subscriptions = CategorySubscription.objects.filter(category=instance.category)
        for subscription in category_subscriptions:
            message = (
                f"Новый заказ в категории '{instance.get_category_display()}':\n"
                f"{instance.title}\n"
                f"Описание: {instance.full_description}\n"
            )
            if instance.price:
                message += f"Цена: {instance.price} MDL\n"
            else:
                message += f"Цена: Договорная\n"
            if instance.deadline:
                message += f"Дедлайн: {instance.deadline.strftime('%d %b %Y')}\n"
            message += f'http://localhost:8000/programmer/order_detail/{instance.id}'
            # message += f'<a href="http://real-domain/programmer/order_detail/{instance.id}/">Открыть заказ</a>'
            send_telegram_notification(message, subscription.user.telegram.telegram_id, TELEGRAM_BOT_TOKEN,
                                       parse_mode="HTML")
    else:
        return 
