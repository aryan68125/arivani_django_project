from django.core.mail import EmailMessage
import os
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
import json
from student.models import *
from marks.models import *
from attendence.models import *
from django.core.mail import send_mail
import pandas as pd

#view sql queries
from django.db import connection
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PostgresLexer
from sqlparse import format
# Create your views here.
def student(request):
    title_ = 'Student'
    data = {
        'title' : title_
    }
    return render(request,'student/student.html',data)

def insert_student_data(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data=json.load(request)
            inserted_values = data.get('payload')
            Student.objects.create(
                 Student_Name = inserted_values['Student_Name'],
                 Father_Name = inserted_values['Father_Name'],
                 roll_no = inserted_values['roll_no'],
                 mobile = inserted_values['mobile'],
                 email = inserted_values['email'],
            )
            print(f"data insert : {inserted_values}")
            return JsonResponse({'status':'data insert successfull'},status=200)
        else:
            return JsonResponse({'status' : 'Error in request'},status=400)
    else:
        return JsonResponse({'status':'something went wrong no ajax request'},status=500)

def read_student_data(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = list(Student.objects.all().values())
            return JsonResponse({'context' : data},status=200)
        else:
            return JsonResponse({'status':'Invalid request'},status=400)
    else:
        return JsonResponse({'status' : 'Error in get data'},status=404)

def update_student_data(request):
    is_ajax = request.headers.get("X-Requested-With") == ('XMLHttpRequest')
    if is_ajax:
        if request.method == "POST":
            data = json.load(request)
            updated_value = data.get('payload')
            print(updated_value)
            try:
                Student_DB_instance = Student.objects.get(pk=updated_value['student_ID'])
                print(Student_DB_instance)
                Student_DB_instance.Student_Name = updated_value['Student_Name']
                Student_DB_instance.Father_Name = updated_value['Father_Name']
                Student_DB_instance.roll_no = updated_value['roll_no']
                Student_DB_instance.mobile = updated_value['mobile']
                Student_DB_instance.email = updated_value['email']
                Student_DB_instance.save()
                return JsonResponse({'status' : 'Data updated successfully!!!'},status=200)
            except Student.DoesNotExist:
                return JsonResponse({'status':'record not found'},status=404)
        else:
            return JsonResponse({'status':'invalid response'},status=400)
    else:
        return JsonResponse({'status':'ajax post is not present'},status=500)

def delete_student_data(request):
    is_ajax = request.headers.get('X-Requested-With')=="XMLHttpRequest"
    if is_ajax:
        if request.method=="POST":
            data=json.load(request)
            deleted_value = data.get('payload')
            print(deleted_value['student_ID'])
            try:
                Student_DB_instance = Student.objects.get(pk=deleted_value['student_ID'])
                print(f"{Student_DB_instance.Student_Name} , {Student_DB_instance.student_ID} deleted")
                Student_DB_instance.delete()
                return JsonResponse({'status':'Data Deleted successfully'},status=200)
            except Student.DoesNotExist:
                return JsonResponse({'status':'Record not found'},status=404)
        else:
            return JsonResponse({'status':'Invalid Request'},status=400)
    else:
        return JsonResponse({'status':'ajax not found'},status=500)
    

# student details page starts
def student_details(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            data = json.load(request)
            student_detail = data.get('payload')
            ID = student_detail['student_ID']
            print(f"student_details function studentID = {ID}")
            return JsonResponse({'status':'Id recieved'},status=400)
        else:
            return JsonResponse({'status':'invalid request'},status=400)
        
def student_details_page(request,ID):
    if ID:
        Student_DB_instance = Student.objects.get(pk=ID)
        try:
            Student_Attendance = Attendance.objects.get(student_ID = ID)
            Student_Marks = Marks.objects.get(Student_ID = ID)
            marks_settings = MarksSettings.objects.first()
            sql_query = connection.queries
            print(sql_query)
            passing_percentage = marks_settings.passing_percentage
            Total_marks_per_subject = marks_settings.Total_marks_per_subject
            Total_Marks = Total_marks_per_subject*6
            data = {
                    'student_ID' : Student_DB_instance.student_ID,
                    'Student_Name' : Student_DB_instance.Student_Name,
                    'Father_Name' : Student_DB_instance.Father_Name, 
                    'roll_no' : Student_DB_instance.roll_no, 
                    'mobile' : Student_DB_instance.mobile,
                    'email' : Student_DB_instance.email,
                    
                    'Maths' : Student_Marks.Maths,
                    'Physics' : Student_Marks.Physics,
                    'Chemistry' : Student_Marks.Chemistry,
                    'Computer' : Student_Marks.Computer,
                    'English' : Student_Marks.English,
                    'Hindi' : Student_Marks.Hindi,
                    'Total_marks_obtained' : Student_Marks.Total_marks_obtained,
                    'Total_Marks' : Total_Marks,
                    'Percentage' : Student_Marks.Percentage,
                    'passing_percentage' : passing_percentage,
                    'pass_fail' : Student_Marks.pass_fail,

                    'date' : Student_Attendance.date,
                    'no_of_days_present' : Student_Attendance.no_of_days_present,
            }
            return render(request,'student/student_details.html',data)
        except Marks.DoesNotExist:
            print("marks does not exist")
            Student_DB_instance = Student.objects.get(pk=ID)
            data = {
                    'student_ID' : Student_DB_instance.student_ID,
                    'Student_Name' : Student_DB_instance.Student_Name,
                    'Father_Name' : Student_DB_instance.Father_Name, 
                    'roll_no' : Student_DB_instance.roll_no, 
                    'mobile' : Student_DB_instance.mobile,
                    'email' : Student_DB_instance.email,
            }
            return render(request,'student/student_details.html',data)
        except Attendance.DoesNotExist:
            print("marks does not exist")
            Student_DB_instance = Student.objects.get(pk=ID)
            data = {
                    'student_ID' : Student_DB_instance.student_ID,
                    'Student_Name' : Student_DB_instance.Student_Name,
                    'Father_Name' : Student_DB_instance.Father_Name, 
                    'roll_no' : Student_DB_instance.roll_no, 
                    'mobile' : Student_DB_instance.mobile,
                    'email' : Student_DB_instance.email,
            }
            return render(request,'student/student_details.html',data)
#send mail using smtp
def send_email(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            data = json.load(request)
            email_data = data.get('payload')
            email_addr = email_data['email']
            marks_data = {
                            "Maths" : email_data['Maths'],
                            "Physics" : email_data['Physics'],
                            "Chemistry" : email_data['Chemistry'],
                            "Computer" : email_data['Computer'],
                            "English" : email_data['English'],
                            "Total_marks_obtained" : email_data['Total_marks_obtained'],
                            "Total_Marks" : email_data['Total_Marks'],
                            "Percentage" : email_data['Percentage'],
                            "passing_percentage" : email_data['passing_percentage'],
                            "pass_fail" : email_data['pass_fail'],
            }
            df = pd.DataFrame(data=marks_data, index=[0])
            df = (df.T)
            print (df)
            # Save DataFrame to Excel file
            excel_file_path = f"/home/aditya/github/django_training/basic_demo_of_django/django_dynamic_url/static/js/student/{email_data['student_name']}_marks.xlsx"
            df.to_excel(excel_file_path)
            
            # Prepare email
            subject = f"{email_data['student_name']}'s Marks are sent from Django"
            message = "Please find attached the marks Excel file."
            recipient_list = [email_addr]

            # Create EmailMessage object and attach the Excel file
            email = EmailMessage(subject, message, 'rollex68125@gmail.com', recipient_list)
            email.attach_file(excel_file_path)

            # Send the email
            email.send()
            print(email_addr)
            email_addr=""
            # Delete the temporary Excel file after sending the email
            os.remove(excel_file_path)

            return JsonResponse({'status': 'email sent'})
# student details page ends