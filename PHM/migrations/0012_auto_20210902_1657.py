# Generated by Django 3.1.7 on 2021-09-02 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHM', '0011_auto_20210902_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rundata',
            name='x_current',
            field=models.CharField(default='0', max_length=30, verbose_name='X相电流'),
        ),
        migrations.AlterField(
            model_name='rundata',
            name='y_current',
            field=models.CharField(default='0', max_length=30, verbose_name='Y相电流'),
        ),
        migrations.AlterField(
            model_name='rundata',
            name='z_current',
            field=models.CharField(default='0', max_length=30, verbose_name='Z相电流'),
        ),
    ]
