from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from hr_app.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from employee.models import *

#make employee json serializable in function "employees_under_hr_list"
from django.core.serializers import serialize
from auth_user.models import *
# Create your views here.
def dashboard_home(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        assigned_user_role = AssignedUserRoles.objects.get(user=user)
        user_role = assigned_user_role.user_role
        if user.is_superuser:
            data = {
                'is_superuser':1,
            }
            return render(request,'hr_app/hr_app_home.html',data)
        else:
            data = {
                'user_role':user_role
            }
            return render(request,'hr_app/hr_app_home.html',data)
    else:
        return redirect("loginUserPage")

def insert_data(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            if request.method == 'POST':
                data = json.load(request)
                f_data = data.get('payload')
                hrID = f_data['hrID']
                name = f_data['name']
                employee_under_Hr = f_data['employee_under_Hr']
                print(employee_under_Hr)
                logged_in_user = request.user.id
                user = User.objects.get(id=logged_in_user)
                if hrID and name:
                    if hrID.isdigit():
                        if int(hrID)>0:
                            db_instance = Hr_model.objects.filter(HrID=hrID, name=name,created_by=user)
                            if db_instance:
                                return JsonResponse({'status':500,'error':'Record Duplication not allowed'},status=500)
                            else:
                                try:
                                    Hr_instance = Hr_model.objects.create(
                                        HrID = hrID,
                                        name = name,
                                        created_by=user,
                                        status=True
                                    )
                                    for employee_id in employee_under_Hr:
                                        employee_instance = Employee.objects.get(pk=employee_id)
                                        Hr_instance.employees_under_hr.add(employee_instance)
                                        
                                    return JsonResponse({'status': 201}, status=201)
                                except:
                                    return JsonResponse({'status': 500,'error':"data can't be inserted"}, status=500)

                        else:
                            return JsonResponse({'status':500,'error':'hrID must not be a negative number'},status=500)
                    else:
                        return JsonResponse({'status':500,'error':'hrID is not a number or a -ve number'},status=500)
                else:
                    return JsonResponse({'status':500,'error':'HrID and name can not be empty'},status=500)
        else:
            return JsonResponse({'status':400,'error':'Bad request'},status=400)
    else:
        return redirect("loginUserPage")

def get_all_data(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            try:
                logged_in_user = request.user.id
                user = User.objects.get(id=logged_in_user)
                Hr_model_var = list(Hr_model.objects.all().filter(is_deleted=0,created_by=user).values())
                #send all employees whos's is_deleted field is false
                employees = list(Employee.objects.all().filter(is_deleted=0).values())

                # send all the employees under hr
                Hrs = Hr_model.objects.all().filter(is_deleted=0,created_by=user)
                employees_under_hr_count={}
                for hr_instance in Hrs:
                    employees_under_hr_count[hr_instance.id] = hr_instance.employees_under_hr.count()

                return JsonResponse({'status':200,'context':Hr_model_var,'employees':employees,'employees_under_hr_count':employees_under_hr_count},status=200)
            except:
                return JsonResponse({'status':500,'error':'Hr_model does not exist'},status=500)
    else:
        return redirect("loginUserPage")

def send_all_employees_under_hr_UPDATE(request):
    if request.user.is_authenticated:
        is_ajax =  request.headers.get("X-Requested-With")=="XMLHttpRequest"
        if is_ajax:
            if request.method=='POST':
                data = json.load(request)
                f_data = data.get('payload')
                hr_id = f_data['id']
                Hrs = Hr_model.objects.get(id=hr_id)
                employee_list_under_hr = []
                for employee in  Hrs.employees_under_hr.all():
                    employee_list_under_hr.append(Employee.objects.get(id=employee.id))   
                
                employee_list = []
                for item in employee_list_under_hr: 
                    employee_dict = {}
                    print (f"employee pk = {item.id} employee id = {item.name}")
                    employee_dict['id'] = item.id
                    employee_dict['name'] = item.name
                    employee_list.append(employee_dict)
                return JsonResponse({'status':200,'context':employee_list},status=200)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
    else:
        return redirect("loginUserPage")
def send_all_employees_reset_dropdown_multiSelect(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            if request.method=='POST':
                employees = list(Employee.objects.all().filter(is_deleted=0).values())
                return JsonResponse({'status':200,'context':employees},status=200)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
    else:
        return redirect("loginUserPage")
def update_data(request):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            if request.method == 'PUT':
                try:
                    data = json.load(request)
                    f_data = data.get('payload')
                    id = f_data['id']
                    hrID = f_data['hrID']
                    name = f_data['name']
                    employee_under_hr_data = f_data['employee_under_Hr']
                    logged_in_user = request.user.id
                    user = User.objects.get(id=logged_in_user)
                    print(f"{f_data}")
                    if hrID and name:
                        if hrID.isdigit():
                            if int(hrID) > 0:
                                try:
                                    db_instance = Hr_model.objects.get(pk=id,created_by=user)
                                    db_instance.HrID = hrID
                                    db_instance.name = name
                                    db_instance.updated_by=user
                                    db_instance.updated_at=timezone.now()
                                    db_instance.status=True
                                    db_instance.save()
                                    for employee in employee_under_hr_data:
                                        employee_instance = Employee.objects.get(pk=employee)
                                        db_instance.employees_under_hr.add(employee_instance)

                                    return JsonResponse({'status': 200},status=200)
                                except Hr_model.DoesNotExist:
                                    return JsonResponse({'status': 404, 'error': 'Record does not exist'}, status=404)
                                except Exception as e:
                                    return JsonResponse({'status': 500, 'error': str(e)}, status=500)
                            else:
                                return JsonResponse({'status': 400, 'error': 'HrID must not be a negative number'}, status=400)
                        else:
                            return JsonResponse({'status': 400, 'error': 'HrID is not a number or a negative number'}, status=400)
                    else:
                        return JsonResponse({'status': 400, 'error': 'HrID and name cannot be empty'}, status=400)
                except json.JSONDecodeError:
                    return JsonResponse({'status': 400, 'error': 'Invalid JSON data'}, status=400)
            else:
                return JsonResponse({'status': 400, 'error': 'Bad Request'}, status=400)
    else:
        return redirect("loginUserPage")

def delete_data(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
        if is_ajax:
            if request.method=='POST':
                try:
                    data = json.load(request)
                    f_data = data.get('payload')
                    id = f_data['id']
                    logged_in_user = request.user.id
                    user = User.objects.get(id=logged_in_user)
                    try:
                        db_instance = Hr_model.objects.get(pk=id,created_by=user)
                        db_instance.is_deleted = 1
                        db_instance.deleted_by = user
                        db_instance.deleted_at = timezone.now()
                        db_instance.save()
                        return JsonResponse({'status':200},status=200)
                    except Hr_model.DoesNotExist:
                        return JsonResponse({'status':404,'error':'Record not found'},status=404)
                except:
                    return JsonResponse({'status':500,'error':'Json error'},status=500)
            else:
                return JsonResponse({'status':500,'error':'Bad Request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'Not an Ajax request'},status=500)
    else:
        return redirect("loginUserPage")

# Recycle bin functionality
def recycle_bin(request):
    if request.user.is_authenticated:
        title = 'hr'
        data={
            'title':title
        }
        return render(request,"recycle_bin/recycle_bin.html",data)
    else:
        return redirect("loginUserPage")

def recycleBinData(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            if request.method=='POST':
                logged_in_user = request.user.id
                user = User.objects.get(id=logged_in_user)
                recycle_bin_data_count = Hr_model.objects.all().filter(is_deleted = 1,created_by=user).count()
                if recycle_bin_data_count:
                    return JsonResponse({'status':200,'count':recycle_bin_data_count},status=200)
                else:
                    return JsonResponse({'status':404,'error':'No data in recycle bin'},status=200)
            else:
                return JsonResponse({'status':400,'error':'bad request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'not ajax'},status=500)
    else:
        return redirect("loginUserPage")

def recyclebin_Data(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
        logged_in_user=request.user.id
        user = User.objects.get(id=logged_in_user)
        if is_ajax:
            if request.method=='POST':
                recycle_bin_data = list(Hr_model.objects.all().filter(is_deleted=1,created_by=user).values())
                return JsonResponse({'status':200,'data':recycle_bin_data},status=200)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'not ajax'},status=500)
    else:
        return redirect("loginUserPage")

def restore_data_hr(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            if request.method=='POST':
                logged_in_user = request.user.id
                user = User.objects.get(id=logged_in_user)
                data = json.load(request)
                f_id = data.get('payload')
                id = int(f_id['id'])
                recycle_bin_data = Hr_model.objects.get(id=id,created_by=user)
                recycle_bin_data.is_deleted=0
                recycle_bin_data.restored_by=user
                recycle_bin_data.restored_at=timezone.now()
                recycle_bin_data.save()
                return JsonResponse({'status':200},status=200)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'not ajax'},status=500)
    else:
        return redirect("loginUserPage")

def delete_data_permanently(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
        if is_ajax:
            if request.method=='POST':
                try:
                    data = json.load(request)
                    f_id = data.get('payload')
                    id = int(f_id['id'])
                    delete_to_data = Hr_model.objects.get(id=id)
                    delete_to_data.delete()
                    return JsonResponse({'status':200},status=200)
                except delete_to_data.DoesNotExist:
                    return JsonResponse({'status':500,'error':'Requested data does not exist'},status=500)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'not ajax'},status=500)
    else:
        return redirect("loginUserPage")
# Recycle bin functionality

# Show employee details working under hr
hr_pk_saved = {}
def employees_under_hr(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            if request.method=='POST':
                try:
                    data = json.load(request)
                    f_data = data.get('payload')
                    hr_pk = f_data['hr_pk']
                    hr_pk_saved.clear()
                    hr_pk_saved['hr_pk'] = hr_pk
                    return JsonResponse({'status':200},status=200)
                except:
                    return JsonResponse({'status':500,'error':'Internal server error'},status=500)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
    else:
        return redirect("loginUserPage")
# open employee_under_hr page

def employees_under_hr_page(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        assigned_user_role = AssignedUserRoles.objects.get(user=user)
        user_role = assigned_user_role.user_role
        data = {
            user_role:user_role
        }
        return render(request,'hr_app/employee_under_hr_page.html',data)
    else:
        return redirect("loginUserPage")

def employees_under_hr_list(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            if request.method=='POST':
                # get all the employees on behalf of hr's p;
                try:
                    hr_pk = hr_pk_saved['hr_pk']
                    Hr_instance = Hr_model.objects.get(id=hr_pk)
                    # print(Hr_instance.name)
                    data = {
                        'hr_name':Hr_instance.name
                    }
                    employee_list_data=[]
                    for employee in Hr_instance.employees_under_hr.all():
                        employee_details = list(Employee.objects.all().filter(id=employee.id).values())
                        employee_list_data.append(employee_details)
                    return JsonResponse({'status':200,'context':employee_list_data,'hr_name':data},status=200)
                except Hr_model.DoesNotExist:
                    return JsonResponse({'status':404,'error':'Hr Does not exist'},status=404)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
    else:
        return redirect("loginUserPage")

def Update_employee_under_hr(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                data = json.load(request)
                f_data = data.get('payload')
                id = f_data['id']
                employeeID = f_data['employeeID']
                employee_name = f_data['employee_name']
                Employee_DB_instance = Employee.objects.get(pk=id)
                Employee_DB_instance.employeeID = employeeID
                Employee_DB_instance.name = employee_name
                if employeeID.isdigit():
                    if int(employeeID)>0:
                        Employee_DB_instance.save()
                        return JsonResponse({'status':200},status=200)
                    else:
                        return JsonResponse({'status':500,'error':'employeeID must be a positive number'},status=500)
                else:
                    return JSonResponse({'status':500,'error':'employeeID is not a digit'},status=500)
            except:
                return JsonResponse({'status':404,'error':'employee does not exist'},status=404)
        else:
            return JsonResponse({'status':400,'error':'Bad request'},status=400)
    else:
        return redirect("loginUserPage")
# Show employee details working under hr