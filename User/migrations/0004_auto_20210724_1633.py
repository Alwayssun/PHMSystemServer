# Generated by Django 3.1.7 on 2021-07-24 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_user_headicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headIcon',
            field=models.CharField(default='static//head//1627106680.92.jpg', max_length=200, verbose_name='头像'),
        ),
    ]