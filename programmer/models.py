from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from customer.models import Order


class Portfolio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    github = models.URLField(blank=True)
    introduction = models.TextField(blank=True)

    education_or_courses = models.TextField(blank=True)
    qualities = models.TextField()
    skills = models.TextField()
    telegram_link_token = models.CharField(max_length=32, blank=True, null=True, unique=True)

    def generate_telegram_token(self):
        self.telegram_link_token = get_random_string(32)
        self.save()
        return self.telegram_link_token

    def __str__(self):
        return 'Портфолио пользователя ' + self.user.first_name + " " + self.user.last_name


class CategorySubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=Order.CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} подписан на обновления {self.category}"


class AuthorSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f"{self.user.first_name} подписан на заказы от {self.author.first_name}"


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram')
    telegram_id = models.CharField(max_length=20, unique=True)
