from django.urls import path
from .views import *


urlpatterns = [
    path('result/input/', InputResultView.as_view(), name='input_result'),
    path('result/student/', StudentResultView.as_view(), name='result_student'),
    path('result/tabulation/<semester_code>/', TabulationSheetTemplate.as_view(), name='result_semester'),
    path('result/download-student-grade-sheet/<registration_number>/', DownloadStudentGradeSheetTemplate.as_view(), name='download_student_grade_sheet'),
    path('result/download-semester-grade-sheet/<semester_code>/', DownloadStudentGradeSheetTemplate.as_view(), name='download_semester_grade_sheet'),
]
