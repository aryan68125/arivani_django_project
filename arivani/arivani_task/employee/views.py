from django.shortcuts import render,redirect
from employee.models import *
from django.urls import reverse
# Create your views here.
def employeePage(request):
        if request.method == 'GET':  # Corrected method check
            employees = Employee.objects.all().filter(is_deleted=0)
            data = {'employees': employees}
            return render(request, 'Employee/employee.html', data)
def create_data(request):
    if request.method=='POST':
        employeeID = request.POST.get('employeeID')
        name = request.POST.get('name')
        if employeeID and name:
            if employeeID.isdigit():
                if int(employeeID)>0:
                    emp = Employee.objects.all().filter(employeeID=employeeID, name=name)
                    if not emp:
                       
                            Employee.objects.create(
                                employeeID=employeeID,
                                name=name
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
ID = {}
def update_data_page(request,pk):
        if request.method == 'GET':  # Corrected method check
            try:
                employee = Employee.objects.get(id=pk)
                employees = Employee.objects.all().filter(is_deleted=0)
                # save id for later use
                ID.clear()
                ID['id']=pk
                return render(request,'Employee/employee.html',{'data':employee,'update':1,'employees':employees})
            except Employee.DoesNotExist:
                return render(request,'Employee/employee.html',{'error':'Employee Does not Exist'})
def update_data(request):
    if request.method=='POST':
        id = ID['id']
        print(f"id : {id}")
        employeeID = request.POST.get('employeeID')
        name = request.POST.get('name')
        if employeeID and name:
            if employeeID.isdigit() and int(employeeID)>0:
                try:
                    employee = Employee.objects.get(id=id)
                    employee.employeeID = employeeID
                    employee.name = name
                    employee.save()
                    return redirect(reverse('update_data_page', kwargs={'pk': id}))
                except Employee.DoesNotExist:
                    return render(request,'Employee/employee.html',{'error':'Employee Does not exist'})
            else:
                return render(request,'Employee/employee.html',{'error':'EmployeeId is not a digit or is -ve'})
        else:
            return render(request,'Employee/employee.html',{'error':'EmployeeId or name is empty'})
    else:
        return render(request,'Employee/employee.html',{'error':'Bad Request'})

def delete_data(request,pk):
    if request.method=='GET':
        try:
            print(f"id : {pk}")
            employee = Employee.objects.get(id=pk)
            employee.is_deleted=1
            employee.save()
            return redirect(reverse('employeePage'))
        except Employee.DoesNotExist:
            return render(request,'Employee/employee.html',{'error':'Employee Does not exist'})
    else:
        return render(request,'Employee/employee.html',{'error':'Bad Request'})
        
