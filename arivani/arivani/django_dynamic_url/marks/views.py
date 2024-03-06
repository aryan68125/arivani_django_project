from django.http import JsonResponse
from django.shortcuts import render
import json
from marks.models import *
from student.models import *
from django.db import transaction
from django.db.utils import OperationalError, IntegrityError
from django.db.models import F, Q
# Create your views here.
def marks(request):
    title_ = 'marks'
    data = {
        'title' : title_
    }
    return render(request,'marks/marks.html',data)

# show student's data starts
def read_student_data(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method == 'POST':
            data = list(Student.objects.all().values())

            return JsonResponse({'context':data},status=200)
        return JsonResponse({'status':'Invalid Response'},status=400)
# show student's data ends
    
# CRUD operations for marks starts
def insert_marks_data(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            data = json.load(request)
            inserted_marks = data.get('payload')
            student = Student.objects.get(pk=inserted_marks['student_ID'])
            Marks_Settings=MarksSettings.objects.get(marks_settings_ID=1)  
            marks_Maths = float(inserted_marks['Maths'])
            marks_Physics = float(inserted_marks['Physics'])
            marks_Chemistry = float(inserted_marks['Chemistry'])
            marks_Computer = float(inserted_marks['Computer'])
            marks_English = float(inserted_marks['English'])
            marks_Hindi = float(inserted_marks['Hindi'])
            Total_marks_per_subject = Marks_Settings.Total_marks_per_subject
            total_obtained_marks = marks_Maths + marks_Physics + marks_Chemistry + marks_Computer + marks_English + marks_Hindi
            percentage = (total_obtained_marks/(Total_marks_per_subject*6))*100
            pass_fail = False
            passing_percentage = Marks_Settings.passing_percentage
            if percentage>=passing_percentage:
                pass_fail = True
            else:
                pass_fail = False
            Marks.objects.create(
                Student_ID = student,
                Student_name = inserted_marks['Student_name'],
                Maths = marks_Maths,
                Physics = marks_Physics,
                Chemistry = marks_Chemistry,
                Computer = marks_Computer,
                English = marks_English,
                Hindi = marks_Hindi,
                Total_marks_obtained = total_obtained_marks,
                Percentage = percentage,
                pass_fail = pass_fail,
            )
            return JsonResponse({'status':'marks inserted successfully'},status=200)
        else:
            return JsonResponse({'status':'Invalid Request'},status=400)
def read_marks_data(request):
    is_ajax = request.headers.get("X-Requested-With")==("XMLHttpRequest")
    if is_ajax:
        if request.method=='POST':
            read_marks_data = list(Marks.objects.all().values())
            read_marks_settings = list(MarksSettings.objects.all().values())
            return JsonResponse({'read_marks_data':read_marks_data, 'read_marks_settings':read_marks_settings},status=200)
        else:
            return JsonResponse({'status':'Invalid response'},status=400)
def update_marks_data(request):
    #update marks not working it's gibing me status 200 but it's not updating the Marks model
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=="POST":
            data = json.load(request)
            updated_marks = data.get('payload')
            try:
                marks_settings = MarksSettings.objects.first()
                passing_percentage = marks_settings.passing_percentage
                Total_marks_per_subject = marks_settings.Total_marks_per_subject
                print(marks_settings.passing_percentage)
                marks_instance = Marks.objects.get(pk=updated_marks['marks_ID'])
                print(marks_instance.Maths)
                Maths = float(updated_marks['Maths'])
                print (Maths)
                Physics = float(updated_marks['Physics'])
                Chemistry = float(updated_marks['Chemistry'])
                Computer = float(updated_marks['Computer'])
                English = float(updated_marks['English'])
                Hindi = float(updated_marks['Hindi'])
                Total_marks_obtained = Maths + Physics + Chemistry + Computer + English + Hindi
                Total_Marks = Total_marks_per_subject*6
                Percentage = (Total_marks_obtained/Total_Marks)*100
                pass_fail = False
                if passing_percentage<=Percentage:
                    pass_fail = True
                else:
                    pass_fail = False
                marks_instance.Maths = Maths
                marks_instance.Physics = Physics
                marks_instance.Chemistry = Chemistry
                marks_instance.Computer = Computer
                marks_instance.English = English
                marks_instance.Hindi = Hindi
                marks_instance.Total_marks_obtained = Total_marks_obtained
                marks_instance.Percentage = Percentage
                marks_instance.pass_fail = pass_fail
                print(marks_instance.Maths)
                marks_instance.save()
                return JsonResponse({'status':'Marks updated successfully'},status=200)
            except Marks.DoesNotExist:
                return JsonResponse({'error':'Marks requested doesnot exist'},status=404)
        else:
            return JsonResponse({'status':'Invalid response'},status=400)
def delete_marks_data(request):
    is_ajax = request.headers.get("X-Requested-With")==("XMLHttpRequest")
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            deleted_data = data.get('payload')
            Marks_to_delete = Marks.objects.get(pk=deleted_data['marks_ID'])
            try:
                Marks_to_delete.delete()
                return JsonResponse({'status':'Marks Deleted successfully'},status=200)
            except Marks.DoesNotExist:
                return JsonResponse({'status':'Marks Does not exist'},status=404)
        else:
            return JsonResponse({'status':'Invalid response'},status=400)

# CRUD operations for marks ends
            
# marks settings starts
def marks_settings(request):
    is_ajax = request.headers.get("X-Requested-With")==("XMLHttpRequest")
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            insert_updated_marks_settings = data.get('payload')
            if insert_updated_marks_settings['marks_settings_ID']:
                    Total_marks_per_subject = float(insert_updated_marks_settings['Total_marks_per_subject'])
                    passing_percentage = float(insert_updated_marks_settings['passing_percentage'])
                    obtained_marks_total = (passing_percentage*(Total_marks_per_subject*6))/100
                    passing_marks_per_subject = obtained_marks_total/6
                    marks = MarksSettings.objects.get(marks_settings_ID=insert_updated_marks_settings['marks_settings_ID'])          
                    marks.marks_settings_ID = insert_updated_marks_settings['marks_settings_ID']
                    marks.passing_percentage = passing_percentage
                    marks.passing_marks_per_subject = passing_marks_per_subject
                    marks.Total_marks_per_subject = Total_marks_per_subject
                    marks.save()
                    print("marks updated")
                    return JsonResponse({'status' : 'Data updated successfully!!!'},status=200)
            else:
                return JsonResponse({'status':'marks_settings_ID not found'},status=404)
        else:
            return JsonResponse({'status' : 'invalid request'},status=500)
def recalculate_pass_fail(request):
    is_ajax = request.headers.get("X-Requested-With")==("XMLHttpRequest")
    if is_ajax:
        if request.method=='POST':
            try:
                with transaction.atomic():
                    marks_settings = MarksSettings.objects.first()
                    passing_percentage = marks_settings.passing_percentage
                    marks = Marks.objects.all()
                    # with transaction.atomic(isolation='read committed'):
                    # for mark in marks:
                    #     percentage_obtained = mark.Percentage
                    #     mark.pass_fail = passing_percentage <= percentage_obtained
                    #     mark.save()
                    Marks.objects.update(
                    pass_fail=Q(Percentage__gte=(passing_percentage))
                )

                return JsonResponse({'status': 'Success'}, status=200)

            except IntegrityError as e:
                # Log the exception or handle it as needed
                return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
        else:
            return JsonResponse({'status':'Invalid Request'},status=400)
# marks settings ends