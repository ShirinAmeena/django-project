from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT')
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Course(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Session_Year(models.Model):
    session_start = models.DateField()
    session_end = models.DateField()

    def __str__(self):
        return f"{self.session_start} To {self.session_end}"


class Student(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.TextField(max_length=100)
    gender = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_year_id = models.ForeignKey(Session_Year,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + ' ' + self.admin.last_name

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.TextField(max_length=100)
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Staff_Notifications(models.Model):
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status  = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.staff_id.admin.first_name

class Student_Notifications(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status  = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.student_id.admin.first_name

class Staff_leave(models.Model):
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    data = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name

class Student_leave(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    data = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name + self.student_id.admin.last_name

class Staff_Feedback(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(blank=True, null=True)  # Allow blank replies
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name

class Student_Feedback(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(blank=True, null=True)  # Allow blank replies
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name + self.student_id.admin.last_name

class Attendance(models.Model):
    subject_id = models.ForeignKey(Subject,on_delete=models.CASCADE)
    attendance_data = models.DateField()
    session_year_id = models.ForeignKey(Session_Year,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject_id.name

class Attendance_Report(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(Attendance,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name

class Student_Result(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_mark = models.IntegerField()
    exam_mark = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.student_id.admin.first_name


