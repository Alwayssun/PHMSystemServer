# Generated by Django 3.2.4 on 2021-07-16 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHM', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]