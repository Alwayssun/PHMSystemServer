# Generated by Django 3.1.7 on 2021-07-24 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20210724_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='headIcon',
            field=models.CharField(default='', max_length=200, verbose_name='头像'),
        ),
    ]
