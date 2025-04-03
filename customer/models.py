from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Order(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Веб-разработка'),
        ('bots', 'Разработка ботов'),
        ('logos', 'Дизайн логотипов'),
        ('mobile', 'Мобильная разработка'),
        ('game', 'Разработка игр'),
        ('data_science', 'Data Science и машинное обучение'),
        ('ai', 'Искусственный интеллект'),
        ('backend', 'Бэкенд-разработка'),
        ('frontend', 'Фронтенд-разработка'),
        ('testing', 'Тестирование ПО'),
        ('other', 'Другое'),
    ]
    title = models.CharField(max_length=250)
    full_description = models.TextField()
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    programmer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='programmer_orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    taken = models.DateTimeField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} + {self.author}"


class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bids')
    description = models.TextField(blank=True)
    programmer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.programmer} for {self.order}"

    def accept(self):
        # Принять заявку и отклонить остальные
        self.status = 'accepted'
        self.save()
        self.order.programmer = self.programmer  # Назначаем программиста
        self.order.save()

        Bid.objects.filter(order=self.order).exclude(id=self.id).update(status='rejected')


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.order.title}"
