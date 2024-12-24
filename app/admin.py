from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Staff_Notifications)
admin.site.register(Staff_leave)
admin.site.register(Staff_Feedback)
admin.site.register(Student_Notifications)
admin.site.register(Student_Feedback)
admin.site.register(Student_leave)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)
admin.site.register(Student_Result)
