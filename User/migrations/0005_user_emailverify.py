# Generated by Django 3.1.7 on 2021-07-24 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_auto_20210724_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emailVerify',
            field=models.CharField(max_length=6, null=True, verbose_name='目前的验证码'),
        ),
    ]
