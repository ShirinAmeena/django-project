from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Course,Session_Year,CustomUser,Student,Staff,Subject,Staff_Notifications,Staff_leave,Staff_Feedback,Student_Notifications,Student_Feedback,Student_leave,Attendance,Attendance_Report,Student_Result
from django.contrib import messages

@login_required(login_url='dologin')
def Student_views(request):
    return render(request,'Student/home.html')

@login_required(login_url='dologin')
def student_notifications(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id
        notification = Student_Notifications.objects.filter(student_id=student_id)

        context = {
            'notification': notification,
        }
    return render(request,'Student/notifications.html',context)

@login_required(login_url='dologin')
def student_notifications_done(request,status):
    notification = Student_Notifications.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('student_notifications')

@login_required(login_url='dologin')
def student_feedback(request):
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id=student_id)
    context ={
        'feedback_history':feedback_history,
    }
    return render(request,'Student/feedback.html',context)


@login_required(login_url='dologin')
def student_save_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')

        student = Student.objects.get(admin=request.user.id)
        feedback = Student_Feedback(
            student_id=student,
            feedback=feedback,
            feedback_reply='',
        )
        feedback.save()
        messages.success(request, 'Feedback Sent Successfully')
        return redirect('student_feedback')  # Redirect to the correct view

    # Fetch the feedback history for consistency
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id=student_id)
    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'Student/feedback.html', context)

@login_required(login_url='dologin')
def student_apply_leave(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id
        student_leave_history = Student_leave.objects.filter(student_id=student_id)
        context = {
            'student_leave_history': student_leave_history,
        }
    return render(request, 'Student/apply_leave.html',context)

@login_required(login_url='dologin')
def student_leave_save(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        student = Student.objects.get(admin=request.user.id)
        leave = Student_leave(
            student_id = student,
            data = leave_date,
            message = leave_message,
        )
        leave.save()
        messages.success(request,'Leave Successfully Sent')
        return redirect('student_apply_leave')
    return render(request, 'Student/apply_leave.html')

@login_required(login_url='dologin')
def student_view_attendance(request):
    student = Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course=student.course_id)
    action = request.GET.get('action')
    get_subject = None
    attendance_report = None  # Initialize the variable to avoid UnboundLocalError

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)
            attendance_report = Attendance_Report.objects.filter(
                student_id=student, attendance_id__subject_id=subject_id
            )

    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
        'attendance_report': attendance_report,
    }
    return render(request, 'Student/view_attendance.html', context)



@login_required(login_url='dologin')
def student_view_result(request):
    mark = None
    student = Student.objects.get(admin = request.user.id)
    result = Student_Result.objects.filter(student_id = student)
    for i in result:
        assignment_mark  = i.assignment_mark
        exam_mark = i.exam_mark
        mark = assignment_mark + exam_mark

    context = {
        'result':result,
        'mark':mark,
    }
    return render(request, 'Student/view_result.html',context)
