# Generated by Django 4.1.3 on 2022-11-28 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffsys', '0003_mobile_info_update_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobile_info',
            name='update_time',
            field=models.DateTimeField(default='-', verbose_name='修改时间'),
        ),
    ]