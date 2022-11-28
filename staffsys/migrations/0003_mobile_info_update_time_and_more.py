# Generated by Django 4.1.3 on 2022-11-28 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffsys', '0002_mobile_info_alter_staff_info_depart'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobile_info',
            name='update_time',
            field=models.DateTimeField(default=0, verbose_name='修改时间'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mobile_info',
            name='create_time',
            field=models.DateTimeField(verbose_name='上传时间'),
        ),
    ]