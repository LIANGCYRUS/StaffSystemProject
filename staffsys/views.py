from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from staffsys import models

def index(request):
    if request.method == 'GET':
        dep_data = models.staff_department.objects.all()
        return render(request, 'index.html',{"dep_data":dep_data})



def add_depart(request):
    if request.method =="GET":
        return render(request, "add_depart.html")

    new_depart = request.POST.get('new_depart')
    models.staff_department.objects.create(title=new_depart)
    return redirect("/depart/")

def delete_depart(request):
    del_id = request.GET.get("nid")
    models.staff_department.objects.filter(id=del_id).delete()
    return redirect("/depart/")
    # return HttpResponse('删除成功')

def edit_depart(request,nid):
    if request.method =='GET':
        edit_obj = models.staff_department.objects.filter(id=nid).first()
        print(edit_obj.title)
        return render(request, "edit_depart.html", {"edit_obj": edit_obj})

    new_depart_name = request.POST.get('new_depart_name')
    models.staff_department.objects.filter(id = nid).update(title=new_depart_name)
    return redirect("/depart/")

def user(request):

    user_data = models.staff_info.objects.all()
    return render(request, "user.html",{"user_data":user_data})

from django import forms
class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.staff_info
        fields = ['name','password','age',"salary","create_time","depart","gender"]
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.TextInput(attrs={"class":"form-control"}),
            "age":forms.TextInput(attrs={"class":"form-control"}),
            "salary":forms.TextInput(attrs={"class":"form-control"}),
            "create_time":forms.TextInput(attrs={"class":"form-control"}),
            "depart":forms.Select(attrs={"class":"form-control"}),
            "gender":forms.Select(attrs={"class":"form-control"}),
        }
def user_add(request):
    '''添加用户 ModelForm'''
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_add.html',{'form':form})

    # 当用户POST提交时,数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/user/')
    else:
        return render(request, 'user_add.html', {'form': form})


def user_edit(request,nid):
    edit_obj = models.staff_info.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据获取的id读取数据库
        form = UserModelForm(instance=edit_obj)
        return  render(request, 'user_edit.html',{"form":form})

    form = UserModelForm(data=request.POST,instance=edit_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/')
    return render(request, 'user_edit.html', {'form':form})


def user_del(request, nid):
    models.staff_info.objects.filter(id = nid).delete()
    return redirect('/user/')