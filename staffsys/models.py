from django.db import models


# Create your models here.
class staff_department(models.Model):
    '''员工部门表'''
    title = models.CharField(verbose_name='标题', max_length=32)

    # 很重要,使其返回是名称而不是对象
    def __str__(self):
        return self.title


class staff_info(models.Model):
    '''员工表'''
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年纪')

    # max_digits = 位数长度、decimal_places = 保留小数点、default = 默认为0
    salary = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')

    depart = models.ForeignKey(to='staff_department', to_field='id', on_delete=models.CASCADE, verbose_name="部门")

    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class Mobile_info(models.Model):
    '''靓号数据'''
    # id 会自动创建
    mobile = models.CharField(verbose_name="手机号码", max_length=11)
    price = models.IntegerField(verbose_name="手机号价格")
    level_choices = (
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),

    )

    level = models.SmallIntegerField(verbose_name='手机号级别', choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )

    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)
    create_time = models.DateTimeField(verbose_name='上传时间')
    # update_time = models.DateTimeField(verbose_name='修改时间', null=True, blank=True)
