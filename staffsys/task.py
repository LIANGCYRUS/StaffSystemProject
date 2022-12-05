from django.shortcuts import render, HttpResponse
from django import forms
from staffsys import models
from django.views.decorators.csrf import csrf_exempt


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title','detail','level']
        widgets={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }





def task_list(request):
    form = TaskModelForm()

    return render(request, "task.html", {"form":form})


# 因为使用ajax，所以要免除 csrf提交。不然会报错
@csrf_exempt
def task_ajax(request):
    print(request.POST)
    return HttpResponse("成功")