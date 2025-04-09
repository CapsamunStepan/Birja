from django.contrib import admin
from .models import Order, Comment, Bid


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_description', 'price', 'category', 'deadline')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('order', 'description', 'programmer', 'status', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'text', 'created')
