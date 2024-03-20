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
    path('get_all_hr/',get_all_hr,name="get_all_hr_manager_views"),
    path('get_all_manager/',get_all_manager,name="get_all_manager_manager_views"),
    path('assign_subordinates/',assign_subordinates,name="assign_subordinates_manager_views"),
    path('get_all_assigned_subordinates/',get_all_assigned_subordinates,name="get_all_assigned_subordinates_manager"),
]
