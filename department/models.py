from django.db import models
from common.models import TrackingModel

class AcademicSession(TrackingModel):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']


class Student(TrackingModel):
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=15, unique=True)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.registration_number
    
    class Meta:
        ordering = ['session', 'registration_number']
    

class Semester(TrackingModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    exam_date = models.DateField(null=True)

    def __str__(self) -> str:
        return self.code
    
    class Meta:
        ordering = ['code']


class Course(TrackingModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credit = models.FloatField(default=1)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['semester']