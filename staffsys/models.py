from django.db import models

# Create your models here.
class staff_department(models.Model):
    '''员工部门表'''
    title = models.CharField(verbose_name='标题', max_length=32)


class staff_info(models.Model):
    '''员工表'''
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年纪')

    # max_digits = 位数长度、decimal_places = 保留小数点、default = 默认为0
    salary = models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')

    depart = models.ForeignKey(to='staff_department', to_field='id', on_delete=models.CASCADE)

    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices)