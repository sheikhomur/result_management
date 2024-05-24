from django.contrib import admin
from .models import *


class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name",
    ]

class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "registration_number", "session"
    ]


class SemesterAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "code", "exam_date"
    ]

class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "code", "credit", "semester", "session"
    ]

admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
