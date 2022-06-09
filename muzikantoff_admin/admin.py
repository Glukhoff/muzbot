import django
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from . import models


# Register your models here.


class PostInline(admin.StackedInline):
    model = models.Post
    extra = 1


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["chat_id", "first_name", "last_name", "created_at", "deleted_at", "is_baned", "is_blocked_bot"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.Menu)
class MenuAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', "parent"]
    inlines = [PostInline]
    resource_class = models.Menu


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["header"]


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["stock_name", "first_name", "last_name", "created_at"]

    def has_add_permission(self, request, obj=None):
        return False
