from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from dashboard.models import *
# Create your views here.
def dashboard_home(request):
    if request.user.is_authenticated:
        return render(request,'dashboard/dashboard_home.html')
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
                if hrID and name:
                    if hrID.isdigit():
                        if int(hrID)>0:
                            db_instance = Hr_model.objects.filter(HrID=hrID, name=name)
                            if db_instance:
                                return JsonResponse({'status':500,'error':'Record Duplication not allowed'},status=500)
                            else:
                                try:
                                    Hr_model.objects.create(
                                        HrID = hrID,
                                        name = name
                                    )
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
        if request.method=='GET':
            try:
                Hr_model_var = list(Hr_model.objects.all().filter(is_deleted=0).values())
                return JsonResponse({'status':200,'context':Hr_model_var},status=200)
            except:
                return JsonResponse({'status':500,'error':'Hr_model does not exist'},status=500)

def update_data(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        if request.method == 'PUT':
            try:
                data = json.load(request)
                f_data = data.get('payload')
                id = f_data['id']
                hrID = f_data['hrID']
                name = f_data['name']
                
                if hrID and name:
                    if hrID.isdigit():
                        if int(hrID) > 0:
                            try:
                                db_instance = Hr_model.objects.get(pk=id)
                                db_instance.HrID = hrID
                                db_instance.name = name
                                db_instance.save()
                                return JsonResponse({'status': 200})
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

def delete_data(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            try:
                data = json.load(request)
                f_data = data.get('payload')
                id = f_data['id']
                try:
                    db_instance = Hr_model.objects.get(pk=id)
                    db_instance.is_deleted = 1
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

