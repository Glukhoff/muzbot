from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Create your models here.


class Person(models.Model):
    chat_id = models.IntegerField(verbose_name="Телеграм ID пользователя", unique=True, editable=False)
    first_name = models.CharField(verbose_name="Фамилия", max_length=50)
    last_name = models.CharField(verbose_name="Имя", max_length=50)
    created_at = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True)
    deleted_at = models.DateTimeField(verbose_name="Дата удаления", null=True, blank=True, editable=False)
    is_baned = models.BooleanField(verbose_name="Пользователь заблокирован", default=False)
    is_blocked_bot = models.BooleanField(verbose_name="Пользователь заблокировал бота", default=False, editable=False)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"


class Menu(MPTTModel):
    title = models.CharField(verbose_name="Название кнопки", max_length=50)
    url = models.URLField(verbose_name="Внешняя ссылка", null=True, blank=True)
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Выберите категорию:"
    )

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = "меню"
        verbose_name_plural = "Меню бота"


class Post(models.Model):
    menu = models.OneToOneField(
        Menu,
        related_name='post',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Выберите категорию:"
    )
    header = models.CharField(verbose_name="Заголовок", max_length=50)
    text = models.TextField(verbose_name="Текст", max_length=4095)
    url = models.URLField(verbose_name="Внешняя ссылка", null=True, blank=True)
    is_stock = models.BooleanField(verbose_name="Это является розыгрышем?", default=False)
    draw_end_date = models.DateTimeField(verbose_name="Дата окончания розыгрыша", null=True, blank=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "посты"
        verbose_name_plural = "Посты"


class Stock(models.Model):
    first_name = models.CharField(verbose_name="Фамилия", max_length=50)
    last_name = models.CharField(verbose_name="Имя", max_length=50)
    stock_name = models.CharField(verbose_name="Название розыгрыша", max_length=50)
    created_at = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    stock_id = models.IntegerField(editable=False)
    participant_id = models.IntegerField(editable=False)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "розыгрыши"
        verbose_name_plural = "Розыгрыши"
