from django.shortcuts import render,redirect
from employee.models import *
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.
def employeePage(request):
    if request.user.is_authenticated:
        logged_in_user=request.user.id
        user = User.objects.get(id=logged_in_user)
        if request.method == 'GET':  # Corrected method check
            employees = Employee.objects.all().filter(is_deleted=0,created_by=logged_in_user)
            employees_deleted = Employee.objects.all().filter(is_deleted=1,created_by=logged_in_user).count()
            
            if user.is_superuser==True:
                data = {
                'employees': employees,
                'employees_deleted':employees_deleted,
                'is_superuser':1
                }
            else:
                data = {
                'employees': employees,
                'employees_deleted':employees_deleted,
                }
            return render(request, 'Employee/employee.html', data)
    else:
        return redirect("loginUserPage")
def create_data(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            employeeID = request.POST.get('employeeID')
            name = request.POST.get('name')
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            if employeeID and name:
                if employeeID.isdigit():
                    if int(employeeID)>0:
                        emp = Employee.objects.all().filter(employeeID=employeeID, name=name,created_by=user)
                        user = User.objects.get(id=logged_in_user)
                        if not emp:
                           
                                Employee.objects.create(
                                    employeeID=employeeID,
                                    name=name,
                                    created_by=user,
                                    status=True,
                                )
                                return redirect(reverse('employeePage'))
                            
                        else:
                            return render(request,'Employee/employee.html',{'error':'employeeID is not unique'})
                    else:
                        return render(request,'Employee/employee.html',{'error':'Employee ID should not be -ve'})
                else:
                    return render(request,'Employee/employee.html',{'error':'EmployeeId is not a digit or is -ve'})
            else:
                return render(request,'Employee/employee.html',{'error':'EmployeeID or name is empty'})
        else:
            return render(request,'Employee/employee.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")
ID = {}
def update_data_page(request,pk):
    if request.user.is_authenticated:
        if request.method == 'GET':  # Corrected method check
            logg_in_user = request.user.id
            user = User.objects.get(id=logg_in_user)
            try:
                employee = Employee.objects.get(id=pk)
                employees = Employee.objects.all().filter(is_deleted=0,created_by=user)
                # save id for later use
                ID.clear()
                ID['id']=pk
                return render(request,'Employee/employee.html',{'data':employee,'update':1,'employees':employees})
            except Employee.DoesNotExist:
                return render(request,'Employee/employee.html',{'error':'Employee Does not Exist'})
    else:
        return redirect("loginUserPage")
def update_data(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            id = ID['id']
            print(f"id : {id}")
            employeeID = request.POST.get('employeeID')
            name = request.POST.get('name')
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            if employeeID and name:
                if employeeID.isdigit() and int(employeeID)>0:
                    try:
                        employee = Employee.objects.get(id=id,created_by=user)
                        employee.employeeID = employeeID
                        employee.updated_at=timezone.now()
                        employee.name = name
                        employee.updated_by=user
                        employee.save()
                        return redirect(reverse('employeePage'))
                        # return redirect(reverse('update_data_page', kwargs={'pk': id}))
                        
                    except Employee.DoesNotExist:
                        return render(request,'Employee/employee.html',{'error':'Employee Does not exist'})
                else:
                    return render(request,'Employee/employee.html',{'error':'EmployeeId is not a digit or is -ve'})
            else:
                return render(request,'Employee/employee.html',{'error':'EmployeeId or name is empty'})
        else:
            return render(request,'Employee/employee.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")

def delete_data(request,pk):
    if request.user.is_authenticated:
        if request.method=='GET':
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            try:
                print(f"id : {pk}")
                employee = Employee.objects.get(id=pk,created_by=user)
                employee.is_deleted=1
                employee.deleted_by=user
                employee.deleted_at=timezone.now()
                employee.save()
                return redirect(reverse('employeePage'))
            except Employee.DoesNotExist:
                return render(request,'Employee/employee.html',{'error':'Employee Does not exist'})
        else:
            return render(request,'Employee/employee.html',{'error':'Bad Request'})
    else:
        return redirect("loginUserPage")

# Recycle bin functionality starts
def recycleBinPage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        if request.method=='GET':
            title = 'emp'
            emp = Employee.objects.all().filter(is_deleted=1,created_by=logged_in_user)
            data={
                'title':title,
                'employees':emp
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
                emp = Employee.objects.get(id=id,created_by=user)
                emp.is_deleted=0
                emp.restored_at = timezone.now()
                emp.restored_by = user
                emp.save()
                return redirect(reverse('recycleBinPage_emp'))
            except:
                title = 'emp'
                emp = Employee.objects.all().filter(is_deleted=1)
                error = 'Data Does not Exist'
                data={
                    'title':title,
                    'employees':emp,
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
            title = "emp"
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
                        emp = Employee.objects.get(id=id)
                        emp.delete()
                        return redirect("recycleBinPage_emp")
                    else:
                        return render(request,'recycle_bin/delete_permanent.html',{'error':'Confirmation messege wrong'})
                else:
                    return render(request,'recycle_bin/delete_permanent.html',{'error':'Input fields can not be empty'})
            except Employee.DoesNotExist:
                return render(request,'recycle_bin/delete_permanent.html',{'error':'Employee Does not Exist'})
        else:
            data = {
                'error':'Bad request'
            }
            return render(request,'recycle_bin/delete_permanent.html',data)
    else:
        return redirect("loginUserPage")
# Recycle bin functionality ends
