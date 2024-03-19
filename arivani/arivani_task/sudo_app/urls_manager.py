from django.urls import path
from sudo_app.views_manager import *
# urlpatterns = [
#     path('hr_page',hr_page,name="hr_page"),
#     path('get_all_employees/',get_all_employees,name="get_all_employees"),
#     path('get_all_hr/',get_all_hr,name="get_all_hr"),
#     path('assign_subordinates/',assign_subordinates,name="assign_subordinates"),
# ]
urlpatterns = [
    path('manager_page/',manager_page,name="manager_page"),
]
