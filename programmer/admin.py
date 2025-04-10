from django.contrib import admin
from .models import Portfolio, CategorySubscription, AuthorSubscription


# Register your models here.
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'github', 'introduction', 'education_or_courses', 'qualities', 'skills')


@admin.register(CategorySubscription)
class CategorySubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')


@admin.register(AuthorSubscription)
class AuthorSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
