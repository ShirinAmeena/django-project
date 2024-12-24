from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Course,Session_Year,CustomUser,Student,Staff,Subject,Staff_Notifications,Staff_leave,Staff_Feedback,Student_Notifications,Student_Feedback,Student_leave,Attendance,Attendance_Report
from django.contrib import messages
@login_required(login_url='dologin')
def Hod_views(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    student_gender_male = Student.objects.filter(gender = 'male').count()
    student_gender_female = Student.objects.filter(gender='female').count()
    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
    }
    return render(request,'HOD/home.html',context)

@login_required(login_url='dologin')
def add_student(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is Already Taken")
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is Already Taken")
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)  # Corrected set_password method
            user.save()

            # Get course and session year instances
            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            # Create the student with the retrieved instances
            student = Student(
                admin=user,
                address=address,
                session_year_id=session_year,
                course_id=course,
                gender=gender
            )
            student.save()
            messages.success(request, user.first_name +" "+ user.last_name + " "+ "Are Successfully Added")
            return redirect('add_student')

    context = {
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'HOD/add_student.html', context)
@login_required(login_url='dologin')
def view_student(request):
    student = Student.objects.all()
    context = {
        'student': student,
    }
    return render(request,'HOD/view_student.html',context)

@login_required(login_url='dologin')
def edit_student(request,id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    context = {
        'student':student,
        'course':course,
        'session_year':session_year,
    }
    return render(request,'HOD/edit_student.html',context)

@login_required(login_url='dologin')
def update_student(request):
    student_id = request.POST.get('student_id')
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id=student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password != None and password != '':
            user.set_password(password)
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id=course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id=session_year_id)
        student.session_year_id = session_year
        student.save()

        messages.success(request,'Records are Successfully Updated')
        return redirect('view_student')
    return render(request,'HOD/edit_student.html')


@login_required(login_url='dologin')
def delete_student(request, admin):
    try:
        student = Student.objects.get(admin_id=admin)
        student.admin.delete()  # Delete the linked CustomUser
        student.delete()  # Delete the Student instance
        messages.success(request, "Records deleted successfully")
    except Student.DoesNotExist:
        messages.error(request, "Student record not found")

    return redirect('view_student')

@login_required(login_url='dologin')
def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request,'Course Added Successfully')
        return redirect('add_course')
    return render(request,'HOD/add_course.html')

@login_required(login_url='dologin')
def view_course(request):
    course = Course.objects.all()
    context = {
        'course':course,
    }
    return render(request,'HOD/view_course.html',context)

@login_required(login_url='dologin')
def edit_course(request,id):
    course = Course.objects.get(id = id)
    context = {
        'course': course,
    }
    return render(request,'HOD/edit_course.html',context)


@login_required(login_url='dologin')
def update_course(request):
    if request.method == 'POST':
        name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        course.name = name
        course.save()
        messages.success(request, 'Course Updated Successfully')
        return redirect('view_course')
    return render(request, 'HOD/edit_course.html')

@login_required(login_url='dologin')
def delete_course(request,id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request,'Course Deleted Successfully')
    return redirect('view_course')

@login_required(login_url='dologin')
def add_staff(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is Already Taken")
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is Already Taken")
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type= 2
            )
            user.set_password(password)  # Corrected set_password method
            user.save()
            staff = Staff(
                admin = user,
                address = address,
                gender = gender

            )
            staff.save()
            messages.success(request,"Staff Added Successfully")
            return redirect('add_staff')
    return render(request, 'HOD/add_staff.html')

@login_required(login_url='dologin')
def view_staff(request):
    staff = Staff.objects.all()
    context = {
        'staff':staff,
    }
    return render(request,'HOD/view_staff.html',context)

@login_required(login_url='dologin')
def edit_staff(request,id):
    staff = Staff.objects.get(id=id)
    context = {
        'staff':staff,
    }
    return render(request,'HOD/edit_staff.html',context)

@login_required(login_url='dologin')
def update_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password != None and password != '':
            user.set_password(password)
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic
        user.save()

        staff = Staff.objects.get(admin = staff_id)
        staff.address = address
        staff.gender = gender
        staff.save()
        messages.success(request,"Staff Updated SuccessFully")
        return redirect('view_staff')
    return render(request,'HOD/edit_staff.html')



@login_required(login_url='dologin')
def delete_staff(request,admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request,'Staff Deleted Successfully')
    return redirect('view_staff')

@login_required(login_url='dologin')
def add_subject(request):
    course = Course.objects.all()
    staff = Staff.objects.all()
    context = {
        'course':course,
        'staff':staff,
    }
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request,"Subject Added SuccessFully")
        return redirect('add_subject')
    return render(request,'HOD/add_subject.html',context)

@login_required(login_url='dologin')
def view_subject(request):
    subject = Subject.objects.all()
    context = {
        'subject':subject,
    }
    return render(request,'HOD/view_subject.html',context)

@login_required(login_url='dologin')
def edit_subject(request,id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    staff = Staff.objects.all()
    context = {
        'subject': subject,
        'course':course,
        'staff':staff,
    }
    return render(request, 'HOD/edit_subject.html', context)

@login_required(login_url='dologin')
def update_subject(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name= request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            id = subject_id,
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request,'Subject Updated SuccessFully')
        return redirect('view_subject')

@login_required(login_url='dologin')
def delete_subject(request,id):
    subject = Subject.objects.filter(id=id)
    subject.delete()
    messages.success(request,'Subject Deleted Successfully')
    return redirect('view_subject')

@login_required(login_url='dologin')
def add_session(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Added Successfully')
        return redirect('add_session')
    return render(request,'HOD/add_session.html')

@login_required(login_url='dologin')
def view_session(request):
    session = Session_Year.objects.all()
    context = {
        'session':session,
    }
    return render(request,'HOD/view_session.html',context)

@login_required(login_url='dologin')
def edit_session(request,id):
    session = Session_Year.objects.get(id=id)
    context = {
        'session':session,
    }
    return render(request,'HOD/edit_session.html',context)

@login_required(login_url='dologin')
def update_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            id = session_id,
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,"Session Updated SuccessFully")
        return redirect('view_session')
    return render(request,'HOD/edit_session.html')

@login_required(login_url='dologin')
def delete_session(request,id):
    session = Session_Year.objects.get(id=id)
    session.delete()
    messages.success(request,'Session Deleted Successfully')
    return redirect('view_session')
@login_required(login_url='dologin')
def send_staff_notifications(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notifications.objects.all().order_by('-id')[0:5]
    context = {
        'staff':staff,
        'see_notification':see_notification,
    }
    return render(request,'Hod/staff_notifications.html',context)
@login_required(login_url='dologin')
def save_staff_notifications(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notifications(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request,'Notifications are successfully sent')
        return redirect('send_staff_notifications')
@login_required(login_url='dologin')
def staff_leave_view(request):
    staff_leave = Staff_leave.objects.all()
    context ={
        'staff_leave':staff_leave,
    }
    return render(request,'Hod/staff_leave_view.html',context)
@login_required(login_url='dologin')
def staff_approve_leave(request,id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')
@login_required(login_url='dologin')
def staff_disapprove_leave(request,id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='dologin')
def staff_feedback_view(request):
    feedback = Staff_Feedback.objects.all()
    feedback_history = Staff_Feedback.objects.all()
    context = {
        'feedback': feedback,
        'feedback_history':feedback_history,
    }
    return render(request,'HOD/staff_feedback.html',context)

@login_required(login_url='dologin')
def staff_feedback_save(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        feedback = Staff_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request, 'Feedback Sent Successfully')
        return redirect('staff_feedback_view')

@login_required(login_url='dologin')
def student_send_notifications(request):
    student = Student.objects.all()
    notification = Student_Notifications.objects.all()
    context = {
        'student':student,
        'notification':notification,
    }
    return render(request,'HOD/student_notifications.html',context)

@login_required(login_url='dologin')
def save_student_notifications(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        student = Student.objects.get(admin = student_id)
        notification = Student_Notifications(
            student_id = student,
            message = message,
        )
        notification.save()
        messages.success(request,'Notifications are successfully sent')
        return redirect('student_send_notifications')

@login_required(login_url='dologin')
def student_feedback_view(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[:5]
    context = {
        'feedback': feedback,
        'feedback_history':feedback_history,
    }
    return render(request,'HOD/student_feedback.html',context)

@login_required(login_url='dologin')
def student_feedback_save(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request,'Feedback Sent Successfully')
        return redirect('student_feedback_view')

def student_leave_view(request):
    student_leave = Student_leave.objects.all()
    context ={
        'student_leave':student_leave,
    }
    return render(request,'Hod/student_leave_view.html',context)

@login_required(login_url='dologin')
def student_approve_leave(request,id):
    leave = Student_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')
@login_required(login_url='dologin')
def student_disapprove_leave(request,id):
    leave = Student_leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')

def view_student_attendance(request):
    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    attendance_report = None
    attendance_data = None

    if action is not None and request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_data = request.POST.get('attendance_data')  # Retrieve attendance date

        # Debugging: Check retrieved data
        print("Subject ID:", subject_id)
        print("Session Year ID:", session_year_id)
        print("Attendance Date:", attendance_data)

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance_report = Attendance_Report.objects.filter(
            attendance_id__subject_id=subject_id,
            attendance_id__session_year_id=session_year_id,
            attendance_id__attendance_data=attendance_data
        )

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action': action,
        'attendance_report': attendance_report,
        'attendance_data': attendance_data,  # Pass attendance date to template
    }
    return render(request, 'Hod/view_student_attendance.html', context)


