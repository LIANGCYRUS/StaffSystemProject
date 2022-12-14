"""StaffSystemProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from staffsys import views, admin, account, task, order

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 部门管理
    path('depart/', views.index),
    path('depart/add/', views.add_depart),
    path('depart/delete/', views.delete_depart),
    path('depart/<int:nid>/edit/', views.edit_depart),

    # 人员管理
    path('user/', views.user),
    path('user/add/', views.user_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/del/', views.user_del),

    # 靓号管理
    path('mobile/', views.mobile),
    path('mobile/add/', views.mobile_add),
    path('mobile/<int:nid>/edit/', views.mobile_edit),
    path('mobile/<int:nid>/del/', views.mobile_del),

    # 管理员管理
    path('admin/', admin.admin_index),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/del/', admin.admin_del),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    # path('admin/<int:nid>/edit/', admin.admin_edit),

    # 账户管理
    path('login/', account.login),
    path('image/code/', account.LoginVerificationCode),

    #     登出管理
    path('logout/', account.logout),

    path('task/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),

    # 订单管理
    path('order/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),

]
