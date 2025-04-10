from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, CategorySubscription
from .utils import send_telegram_notification


@receiver(post_save, sender=Order)
def notify_subscribers_on_new_order(sender, instance, created, **kwargs):
    if created:
        category_subscriptions = CategorySubscription.objects.filter(category=instance.category)
        for subscription in category_subscriptions:
            message = (
                f"Новый заказ в категории {instance.get_category_display()}:\n"
                f"{instance.title}\n"
                f"Описание: {instance.full_description}\n"
            )
            if instance.price:
                message += f"Цена: {instance.price} MDL\n"
            else:
                message += f"Цена: Договорная\n"
            if instance.deadline:
                message += f"Дедлайн: {instance.deadline}"
            send_telegram_notification(message, 'subscription.user.telegram.user_id', 'token')
    else:
        return 
