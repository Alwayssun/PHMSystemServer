# Generated by Django 3.1.7 on 2021-09-02 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHM', '0009_auto_20210724_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('data', models.CharField(max_length=30, verbose_name='数据')),
                ('status', models.CharField(max_length=5, verbose_name='故障状态')),
            ],
            options={
                'verbose_name': '数据',
                'verbose_name_plural': '数据',
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
