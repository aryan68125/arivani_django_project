from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from manager.models import *

from django.contrib import messages
# Create your views here.

def ManagerPage(request):
    if request.user.is_authenticated:
        logged_in_user=request.user.id
        if request.method == 'GET':  # Corrected method check
            manager = ManagerModel.objects.all().filter(is_deleted=0,created_by=logged_in_user)
            manager_deleted = ManagerModel.objects.all().filter(is_deleted=1,created_by=logged_in_user).count()
            data = {
                'managers': manager,
                'manager_deleted':manager_deleted
                }
            return render(request, 'manager/manager.html', data)
    else:
        return redirect("loginUserPage")
def create_data(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            managerID = request.POST.get('managerID')
            name = request.POST.get('name')
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            if managerID and name:
                if managerID.isdigit():
                    if int(managerID)>0:
                        manager = ManagerModel.objects.all().filter(managerID=managerID, name=name,created_by=user)
                        user = User.objects.get(id=logged_in_user)
                        if not manager:
                           
                                ManagerModel.objects.create(
                                    managerID=managerID,
                                    name=name,
                                    created_by=user,
                                    status=True,
                                )
                                return redirect(reverse('ManagerPage'))
                            
                        else:
                            return render(request,'manager/manager.html',{'error':'Manager ID is not unique'})
                    else:
                        return render(request,'manager/manager.html',{'error':'Manager ID should not be -ve'})
                else:
                    return render(request,'manager/manager.html',{'error':'Manager ID is not a digit or is -ve'})
            else:
                return render(request,'manager/manager.html',{'error':'Manager ID or name is empty'})
        else:
            return render(request,'manager/manager.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")
ID = {}
def update_data_page(request,pk):
    if request.user.is_authenticated:
        if request.method == 'GET':  # Corrected method check
            logg_in_user = request.user.id
            user = User.objects.get(id=logg_in_user)
            try:
                manager = ManagerModel.objects.get(id=pk)
                managers = ManagerModel.objects.all().filter(is_deleted=0,created_by=user)
                # save id for later use
                ID.clear()
                ID['id']=pk
                print(f"ID saved = {ID['id']}")
                return render(request,'manager/manager.html',{'data':manager,'update':1,'managers':managers})
            except ManagerModel.DoesNotExist:
                return render(request,'manager/manager.html',{'error':'Manager Does not Exist'})
    else:
        return redirect("loginUserPage")
def update_data(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            id = ID['id']
            print(f"id : {id}")
            managerID = request.POST.get('managerID')
            name = request.POST.get('name')
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            if managerID and name:
                if managerID.isdigit() and int(managerID)>0:
                    try:
                        manager = ManagerModel.objects.get(id=id,created_by=user)
                        manager.managerID = managerID
                        manager.updated_at=timezone.now()
                        manager.name = name
                        manager.updated_by=user
                        manager.save()
                        return redirect(reverse('ManagerPage'))
                        # return redirect(reverse('update_data_page', kwargs={'pk': id}))
                        
                    except Employee.DoesNotExist:
                        return render(request,'manager/manager.html',{'error':'Manager Does not exist'})
                else:
                    return render(request,'manager/manager.html',{'error':'ManagerId is not a digit or is -ve'})
            else:
                return render(request,'manager/manager.html',{'error':'ManagerId or name is empty'})
        else:
            return render(request,'manager/manager.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")

def delete_data(request,pk):
    if request.user.is_authenticated:
        if request.method=='GET':
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            try:
                print(f"id : {pk}")
                manager = ManagerModel.objects.get(id=pk,created_by=user)
                manager.is_deleted=1
                manager.deleted_by=user
                manager.deleted_at=timezone.now()
                manager.save()
                return redirect(reverse('ManagerPage'))
            except Employee.DoesNotExist:
                return render(request,'manager/manager.html',{'error':'Manager Does not exist'})
        else:
            return render(request,'manager/manager.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")

# Recycle bin functionality starts
def recycleBinPage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        if request.method=='GET':
            title = 'manager'
            manager = ManagerModel.objects.all().filter(is_deleted=1,created_by=logged_in_user)
            data={
                'title':title,
                'managers':manager
            }
            return render(request,'recycle_bin/recycle_bin.html',data)
        else:
            return render(request, 'recycle_bin/recycle_bin.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")
def restoreData_emp(request,pk):
    if request.user.is_authenticated:
        if request.method=='GET':
            id=int(pk)
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            try:
                manager = ManagerModel.objects.get(id=id,created_by=user)
                manager.is_deleted=0
                manager.restored_at = timezone.now()
                manager.restored_by = user
                manager.save()
                return redirect(reverse('recycleBinPage_manager'))
            except:
                title = 'manager'
                manager = ManagerModel.objects.all().filter(is_deleted=1)
                error = 'Data Does not Exist'
                data={
                    'title':title,
                    'managers':manager,
                    'error':error
                }
                return render(request,'recycle_bin/recycle_bin.html',data)
        else:
            return render(request, 'recycle_bin/recycle_bin.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")
delete_data_perma = {}
def deleteDataPermanentlyPage(request,pk):
    if request.user.is_authenticated:
        if request.method=='GET':
            delete_data_perma.clear()
            delete_data_perma['id'] = pk
            print(f"permanent delete id : {delete_data_perma['id']}")
            title = "manager"
            data = {
                'title':title
            }
            return render(request,'recycle_bin/delete_permanent.html',data)
        else:
            return render(request,'recycle_bin/delete_permanent.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")
def deleteDataPermanently(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            id = delete_data_perma['id']
            c_msg = request.POST.get('delete_text')
            try:
                if c_msg:
                    if c_msg == "DELETE":
                        manager = ManagerModel.objects.get(id=id)
                        manager.delete()
                        return redirect("recycleBinPage_manager")
                    else:
                        messages.error(request, 'Confirmation messege wrong')
                        return render(request,'recycle_bin/delete_permanent.html')
                        # return render(request,'recycle_bin/delete_permanent.html',{'error':'Confirmation messege wrong'})
                else:
                    messages.error(request, 'Input fields can not be empty')
                    return render(request,'recycle_bin/delete_permanent.html')
                    # return render(request,'recycle_bin/delete_permanent.html',{'error':'Input fields can not be empty'})
            except Employee.DoesNotExist:
                messages.error(request, 'Employee Does not Exist')
                return render(request,'recycle_bin/delete_permanent.html')
                # return render(request,'recycle_bin/delete_permanent.html',{'error':'Employee Does not Exist'})
        else:
            # data = {
            #     'error':'Bad request'
            # }
            messages.error(request, 'Bad request')
            return render(request,'recycle_bin/delete_permanent.html')
            # return render(request,'recycle_bin/delete_permanent.html',data)
    else:
        return redirect("loginUserPage")
# Recycle bin functionality ends


