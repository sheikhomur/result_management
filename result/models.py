from django.db import models
from common.models import TrackingModel


class Result(TrackingModel):
    course = models.ForeignKey('department.Course', on_delete=models.CASCADE)
    semester = models.ForeignKey('department.Semester', on_delete=models.CASCADE)
    session = models.ForeignKey('department.AcademicSession', on_delete=models.CASCADE)
    student = models.ForeignKey('department.Student', on_delete=models.CASCADE)
    tt_mark = models.FloatField(default=0)
    attendance = models.FloatField(default=0)
    final_evaluation = models.FloatField(default=0)
