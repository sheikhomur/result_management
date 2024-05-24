from django.urls import path
from .views import *


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    path('courses/', CourseListPage.as_view(), name='list_courses'),
    path('create-course/', CourseCreatePage.as_view(), name='create_course'),
    
    path('students/', StudentListPage.as_view(), name='list_students'),
    path('create-student/', StudentCreatePage.as_view(), name='create_student'),
    
    path('semesters/', SemesterListPage.as_view(), name='list_semesters'),
    path('create-semester/', SemesterCreatePage.as_view(), name='create_semester'),

    path('sessions/', AcademicSessionListPage.as_view(), name='list_sessions'),
    path('create-session/', AcademicSessionCreatePage.as_view(), name='create_session'),
]
