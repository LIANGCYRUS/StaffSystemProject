from django.shortcuts import render, HttpResponse
from staffsys import models
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, Page


def get_page_range(num, total_page, size=7):
    '''
    :param num: 当前页数
    :param total_page: 总页数
    :param size: 列表的数量，即 上一页 [1,2,3,4,5,6,7] 下一页
    :return:
    '''

    #
    min = num - int(size / 2)
    min = min if min >= 1 else 1
    max = min + size - 1
    max = max if max <= total_page else total_page
    return range(min, max + 1)


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['oid', 'sku_title', 'price', 'status', "order_time"]
        widgets = {
            'oid': forms.TextInput(attrs={'class': 'form-control'}),
            'sku_title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            "order_time": forms.TextInput(attrs={'class': 'form-control'})
        }


def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')
    form = OrderModelForm()

    # 获取需要显示的页数
    page = request.GET.get('page')

    # 使用django自带的分页类 Paginator，在传参中，第一项是数据库对象，二项是每页显示的条数，
    # 表示从数据库导出来的信息，以15条（第二个参数）进行显示。
    paginator = Paginator(queryset, 15)

    # .get_page()是获得当前页数的数据，这个方法的好处是，如果输入大于页数的数，也只会显示最大页数。输入不是数字的，就会显示第一页。十分方便不需要做判断。
    mobile_paginator = paginator.get_page(page)

    # 分页页数
    page_range = get_page_range(mobile_paginator.number, paginator.num_pages, 7)

    # ********** 分页处理 - 结束 ********** #

    context = {
        'data': mobile_paginator,
        'page_range': page_range,
        "form": form
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)

    form.instance.sys_upload_admin_id = request.session["info"]["id"]

    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)

    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)


def order_delete(request):
    # 在前端ajax拿到uid
    uid = request.GET.get("uid")
    # 在数据库查看是否存在
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})
