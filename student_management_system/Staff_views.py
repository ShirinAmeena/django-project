from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Staff,Staff_Notifications,Staff_leave,Subject,Session_Year,Student,Attendance,Attendance_Report,Staff_Feedback,Student_Result
from django.contrib import messages
@login_required(login_url='dologin')
def Staff_views(request):
    return render(request,'Staff/home.html')
@login_required(login_url='dologin')

def notifications(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        notification = Staff_Notifications.objects.filter(staff_id = staff_id)

        context = {
            'notification':notification,
        }
    return render(request,'Staff/notifications.html',context)
@login_required(login_url='dologin')
def notifications_done(request,status):
    notification = Staff_Notifications.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('notifications')
@login_required(login_url='dologin')
def apply_leave(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)
        context = {
            'staff_leave_history': staff_leave_history,
        }
    return render(request, 'Staff/apply_leave.html', context)

@login_required(login_url='dologin')
def add_apply_leave(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        staff = Staff.objects.get(admin=request.user.id)
        leave = Staff_leave(
            staff_id = staff,
            data = leave_date,
            message = leave_message,
        )
        leave.save()
        messages.success(request,'Leave Successfully Sent')
        return redirect('apply_leave')

@login_required(login_url='dologin')
def staff_feedback(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)
    context ={
        'feedback_history':feedback_history,
    }
    return render(request,'Staff/feedback.html',context)

@login_required(login_url='dologin')
def save_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        staff = Staff.objects.get(admin = request.user.id)
        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply = '',
        )
        feedback.save()
        messages.success(request,'Feedback Sent Successfully')
        return redirect('staff_feedback')
    return render(request, 'Staff/feedback.html')

@login_required(login_url='dologin')
def staff_take_attendance(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff = staff_id)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    students = None
    if action is not None:
        if request.method == 'POST':
            subject_id  = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            subject = Subject.objects.filter(id=subject_id)

            for i in subject:
                student_id  = i.course.id
                students = Student.objects.filter(course_id=student_id)
    context ={
        'subject':subject,
        'session_year':session_year,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'action': action,
        'students':students,
    }
    return render(request,'Staff/take_attendance.html',context)


@login_required(login_url='dologin')
def staff_save_attendance(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_data = request.POST.get('attendance_data')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance =Attendance(
            subject_id = get_subject,
            attendance_data = attendance_data,
            session_year_id = get_session_year,
        )
        attendance.save()
        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)
            p_students = Student.objects.get(id=int_stud)
            attendance_report = Attendance_Report(
                student_id = p_students,
                attendance_id = attendance,
            )
            attendance_report.save()
            messages.success(request,'Attendance Added Successfully')
        return redirect('staff_take_attendance')

@login_required(login_url='dologin')
def staff_view_attendance(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff_id=staff_id)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    attendance_data = None
    attendance_report = None
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_data = request.POST.get('attendance_data')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)
        attendance = Attendance.objects.filter(subject_id=get_subject,attendance_data=attendance_data)
        for i in attendance:
            attendance_id = i.id
            attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'subject':subject,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'attendance_data':attendance_data,
        'attendance_report':attendance_report,
    }
    return render(request,'Staff/view_attendance.html',context)

@login_required(login_url='dologin')
def add_result(request):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff_id=staff)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    students = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            subjects = Subject.objects.filter(id=subject_id)
            for i in subjects:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)
    context ={
        'subjects':subjects,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'students':students,

    }
    return render(request,'Staff/add_result.html',context)
@login_required(login_url='dologin')
def save_result(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        exam_mark = request.POST.get('exam_mark')

        print(f"Received student_id: {student_id}, subject_id: {subject_id}")

        try:
            get_student = Student.objects.get(admin=student_id)
        except Student.DoesNotExist:
            messages.error(request, f"Student with ID {student_id} does not exist.")
            return redirect('add_result')

        get_subject = Subject.objects.get(id=subject_id)

        check_exists = Student_Result.objects.filter(
            subject_id=get_subject, student_id=get_student
        ).exists()

        if check_exists:
            result = Student_Result.objects.get(
                subject_id=get_subject, student_id=get_student
            )
            result.assignment_mark = assignment_mark
            result.exam_mark = exam_mark
            result.save()
            messages.success(request, 'Result successfully updated.')
        else:
            result = Student_Result(
                student_id=get_student,
                subject_id=get_subject,
                exam_mark=exam_mark,
                assignment_mark=assignment_mark,
            )
            result.save()
            messages.success(request, 'Result successfully added.')

        return redirect('add_result')

    return render(request, 'Staff/add_result.html')


