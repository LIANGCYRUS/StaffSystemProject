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