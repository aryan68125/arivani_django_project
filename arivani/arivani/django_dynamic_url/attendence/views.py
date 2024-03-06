from django.http import JsonResponse
from django.shortcuts import render
import json
from attendence.models import *
from student.models import *
from datetime import datetime
# Create your views here.
def attendance(request):
    title_ = "Attendance"
    data={
        'title':title_
    }
    return render(request,'attendance/attendance.html',data)
def insert_attendance(request):
    is_ajax = request.headers.get("X-Requested-With") == ('XMLHttpRequest')
    if is_ajax:
        if request.method=='POST':
            data = json.load(request)
            inserted_attendance = data.get('payload')
            try:
                Student_instance = Student.objects.get(pk=inserted_attendance['student_ID'])
                # Assuming your date string is in a different format
                date_string = inserted_attendance['date_selected']
                
                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_string, "%Y-%m-%d")
                
                # Format the datetime object in the "YYYY-MM-DD" format
                formatted_date = date_object.strftime("%Y-%m-%d")
                Attendance.objects.create(
                    date = formatted_date,
                    no_of_days_present = inserted_attendance['no_of_days_present'],
                    student_ID = Student_instance,
                    Student_Name = inserted_attendance['Student_Name'],
                )
                return JsonResponse({'status':200},status=200)
            except:
                return JsonResponse({'status':500},status=500)
        return JsonResponse({'status':'Invalid request'},status=400)
    return JsonResponse({'status':'ajax error'},status=599)
def Read_attendance(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=="POST":
            attendace_data = list(Attendance.objects.all().values())
            return JsonResponse({'context':attendace_data},status=200)
        else:
            return JsonResponse({'status':'Invalid request'},status=400)
def get_student_data(request):
    is_ajax = request.headers.get('X-Requested-With')=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            Student_data=list(Student.objects.all().values())
            return JsonResponse({'context':Student_data},status=200)
        return JsonResponse({'status':'invalid request'},status=400)
    return JsonResponse({'status':'ajax error'},status=506)
def update_attendance(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=="POST":
            data = json.load(request)
            updated_data = data.get('payload')
            try:
                Student_instance = Student.objects.get(pk=updated_data['student_ID'])
                Attendance_instance = Attendance.objects.get(pk=updated_data['attendance_ID'])
                Attendance_instance.student_ID = Student_instance
                Attendance_instance.date = updated_data['date']
                Attendance_instance.no_of_days_present = updated_data['no_of_days_present']
                Attendance_instance.save()
                return JsonResponse({'status':'attendance updated successfully!!!'},status=200)
            except Attendance.DoesNotExist:
                return JsonResponse({'status':'data does not exist'},status=404)
        else:
            return JsonResponse({'status':'invalid request'},status=400)
def delete_attendance(request):
    is_ajax=request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            data_delete = data.get('payload')
            try:
                Attendance_instnace = Attendance.objects.get(pk=data_delete['attendance_ID'])
                Attendance_instnace.delete()
                return JsonResponse({'status':'attendace deleted successfully!!!'},status=200)
            except Attendance_instnace.DoesNotExist:
                return JsonResponse({'status':'dattendace does not exist'},status=404)
        return JsonResponse({'status':'invalid request'},status=400)