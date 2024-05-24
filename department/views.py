from django.shortcuts import render
from django.views import View
from department.forms import AcademicSessionForm, CourseForm, SemesterForm, StudentForm
from department.models import AcademicSession, Course, Semester, Student
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'department/dashboard.html')


class CourseListPage(LoginRequiredMixin, View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'department/courses.html', {'courses': courses})


class CourseCreatePage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "department/create_course.html"
    success_url = reverse_lazy('list_courses')
    success_message = "Course created successfully!"

    def post(self, request):
        return super().post(request)


class SemesterListPage(LoginRequiredMixin, View):
    def get(self, request):
        semesters = Semester.objects.order_by('code')
        return render(request, 'department/semesters.html', {'semesters': semesters})


class SemesterCreatePage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = "department/create_semester.html"
    success_url = reverse_lazy('list_semesters')
    success_message = "Semester created successfully!"

class StudentListPage(LoginRequiredMixin, View):
    def get(self, request):
        students = Student.objects.order_by('registration_number')
        return render(request, 'department/students.html', {'students': students})


class StudentCreatePage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "department/create_student.html"
    success_url = reverse_lazy('list_students')
    success_message = "Student created successfully!"


class AcademicSessionListPage(LoginRequiredMixin, View):
    def get(self, request):
        sessions = AcademicSession.objects.order_by('name')
        return render(request, 'department/sessions.html', {'sessions': sessions})


class AcademicSessionCreatePage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "department/create_session.html"
    success_url = reverse_lazy('list_sessions')
    success_message = "Session created successfully!"
