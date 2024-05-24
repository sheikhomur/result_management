from django import forms
from .models import AcademicSession, Course, Semester, Student


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class AcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = "__all__"

