# Generated by Django 4.0.5 on 2022-06-09 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muzikantoff_admin', '0003_alter_post_draw_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='draw_end_date',
            field=models.DateTimeField(blank=None, default=None, null=True, verbose_name='Дата окончания розыгрыша'),
        ),
        migrations.AlterField(
            model_name='post',
            name='header',
            field=models.CharField(max_length=50, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(max_length=4095, verbose_name='Текст'),
        ),
    ]
