from django.contrib import admin
from .models import Portfolio, CategorySubscription, AuthorSubscription, TelegramUser


# Register your models here.
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'github', 'introduction', 'education_or_courses', 'qualities', 'skills',
                    'telegram_link_token')


@admin.register(CategorySubscription)
class CategorySubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')


@admin.register(AuthorSubscription)
class AuthorSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id')
