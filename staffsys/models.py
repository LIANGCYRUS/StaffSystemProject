from django.db import models


# Create your models here.
class staff_department(models.Model):
    """员工部门表"""
    title = models.CharField(verbose_name='标题', max_length=32)

    # 很重要,使其返回是名称而不是对象
    def __str__(self):
        return self.title


class staff_info(models.Model):
    """员工表"""
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
    """靓号数据"""
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


class AdminInfo(models.Model):
    """管理员 数据库表"""
    username = models.CharField(verbose_name="管理员名", max_length=16)
    password = models.CharField(verbose_name="管理员密码", max_length=200)


class Task(models.Model):
    title = models.CharField(verbose_name="任务名称", max_length=64)
    detail = models.TextField(verbose_name="任务内容")
    level_choice = ((1, '紧急'), (2, '重要'), (3, '一般'),)
    level = models.SmallIntegerField(verbose_name='任务等级', choices=level_choice, default=1)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class Order(models.Model):
    """工单"""
    oid = models.CharField(verbose_name="订单号", max_length=64)
    sku_title = models.CharField(verbose_name="产品名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1,"待支付"),
        (2,"已付款"),
    )
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices, default=1)
    order_time = models.DateTimeField(verbose_name="付款时间",)
    # sys_upload_time = models.DateTimeField(verbose_name="上传时间",auto_now_add=True)
    sys_upload_admin = models.ForeignKey(verbose_name="上传者", to="AdminInfo", on_delete=models.CASCADE)
