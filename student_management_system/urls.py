
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views,Hod_views,Staff_views,Student_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('base/',views.base,name='base'),
    path('dologin/', views.dologin, name='dologin'),
    path('dologout/', views.dologout, name='dologout'),
    # HOD Views
    path('hod/home', Hod_views.Hod_views, name='hod_home'),
    # HOD notification
    path('send_staff_notifications', Hod_views.send_staff_notifications, name='send_staff_notifications'),
    path('save_staff_notifications', Hod_views.save_staff_notifications, name='save_staff_notifications'),
    path('student_send_notifications',Hod_views.student_send_notifications, name='student_send_notifications'),
    path('save_student_notifications', Hod_views.save_student_notifications, name='save_student_notifications'),
    # HOD Leave
    path('staff_leave_view',Hod_views.staff_leave_view,name='staff_leave_view'),
    path('staff_approve_leave/<str:id>',Hod_views.staff_approve_leave,name='staff_approve_leave'),
    path('staff_disapprove_leave/<str:id>',Hod_views.staff_disapprove_leave,name='staff_disapprove_leave'),
    path('student_leave_view',Hod_views.student_leave_view,name='student_leave_view'),
    path('student_approve_leave/<str:id>', Hod_views.student_approve_leave, name='student_approve_leave'),
    path('student_disapprove_leave/<str:id>', Hod_views.student_disapprove_leave, name='student_disapprove_leave'),
    #HOD staff feedback
    path('staff_feedback_view', Hod_views.staff_feedback_view, name='staff_feedback_view'),
    path('staff_feedback_save', Hod_views.staff_feedback_save, name='staff_feedback_save'),
    #HOD student feedback
    path('student_feedback_view', Hod_views.student_feedback_view, name='student_feedback_view'),
    path('student_feedback_save', Hod_views.student_feedback_save, name='student_feedback_save'),
    #HOD view student attendance
    path('view_student_attendance', Hod_views.view_student_attendance, name='view_student_attendance'),
    #Student
    path('add_student/', Hod_views.add_student, name='add_student'),
    path('view_student/', Hod_views.view_student, name='view_student'),
    path('edit_student/<str:id>', Hod_views.edit_student, name='edit_student'),
    path('update_student/', Hod_views.update_student, name='update_student'),
    path('delete_student/<str:admin>', Hod_views.delete_student, name='delete_student'),
    #Staff
    path('add_staff/', Hod_views.add_staff, name='add_staff'),
    path('view_staff/', Hod_views.view_staff, name='view_staff'),
    path('edit_staff/<str:id>', Hod_views.edit_staff, name='edit_staff'),
    path('update_staff/', Hod_views.update_staff, name='update_staff'),
    path('delete_staff/<str:admin>', Hod_views.delete_staff, name='delete_staff'),
    #Subject
    path('add_subject/', Hod_views.add_subject, name='add_subject'),
    path('view_subject/', Hod_views.view_subject, name='view_subject'),
    path('edit_subject/<str:id>', Hod_views.edit_subject, name='edit_subject'),
    path('update_subject/', Hod_views.update_subject, name='update_subject'),
    path('delete_subject/<str:id>', Hod_views.delete_subject, name='delete_subject'),
    #session
    path('add_session/', Hod_views.add_session, name='add_session'),
    path('view_session/', Hod_views.view_session, name='view_session'),
    path('edit_session/<str:id>', Hod_views.edit_session, name='edit_session'),
    path('update_session/', Hod_views.update_session, name='update_session'),
    path('delete_session/<str:id>', Hod_views.delete_session, name='delete_session'),
    #profile
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    #course
    path('add_course/', Hod_views.add_course, name='add_course'),
    path('view_course/', Hod_views.view_course, name='view_course'),
    path('edit_course/<str:id>', Hod_views.edit_course, name='edit_course'),
    path('update_course/', Hod_views.update_course, name='update_course'),
    path('delete_course/<int:id>/', Hod_views.delete_course, name='delete_course'),

    # Staff
    path('staff/home', Staff_views.Staff_views, name='staff_home'),
    path('notifications', Staff_views.notifications, name='notifications'),
    path('notifications_done/<str:status>', Staff_views.notifications_done, name='notifications_done'),
    path('apply_leave', Staff_views.apply_leave, name='apply_leave'),
    path('add_apply_leave', Staff_views.add_apply_leave, name='add_apply_leave'),
    path('staff_feedback', Staff_views.staff_feedback, name='staff_feedback'),
    path('save_feedback', Staff_views.save_feedback, name='save_feedback'),
    path('staff_take_attendance', Staff_views.staff_take_attendance, name='staff_take_attendance'),
    path('staff_save_attendance', Staff_views.staff_save_attendance, name='staff_save_attendance'),
    path('staff_view_attendance', Staff_views.staff_view_attendance, name='staff_view_attendance'),
    path('add_result', Staff_views.add_result, name='add_result'),
    path('save_result', Staff_views.save_result, name='save_result'),


    # student
    path('student/home', Student_views.Student_views, name='student_home'),
    path('student_notifications', Student_views.student_notifications, name='student_notifications'),
    path('student_notifications_done/<str:status>', Student_views.student_notifications_done, name='student_notifications_done'),
    path('student_feedback', Student_views.student_feedback, name='student_feedback'),
    path('student_save_feedback', Student_views.student_save_feedback, name='student_save_feedback'),
    path('student_apply_leave', Student_views.student_apply_leave, name='student_apply_leave'),
    path('student_leave_save', Student_views.student_leave_save, name='student_leave_save'),
    path('student_view_attendance', Student_views.student_view_attendance, name='student_view_attendance'),
    path('student_view_result', Student_views.student_view_result, name='student_view_result'),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

