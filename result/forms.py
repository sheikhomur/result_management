from django import forms
from department.models import AcademicSession, Course, Semester
from result.models import Result

class StudentResultForm(forms.Form):
    registration_number = forms.CharField(
        label='Registration Number', max_length=10,
        widget=forms.TextInput(attrs={'class': "form-control", "placeholder": "Registration number..."})
    )


def get_courses():
    courses = Course.objects.all()
    return [[course.name, course.name] for course in courses]

def get_academic_sessions():
    sessions = AcademicSession.objects.all()
    return [[session.name, session.name] for session in sessions]

def get_semesters():
    semesters = Semester.objects.all()
    return [[semester.name, semester.name] for semester in semesters]


class ResultItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResultItemForm, self).__init__(*args, **kwargs)
        self.fields['student'].label = ""
        self.fields['tt_mark'].label = ""
        self.fields['attendance'].label = ""
        self.fields['final_evaluation'].label = ""
    
    class Meta:
        model = Result
        fields = ["student", "tt_mark", "attendance", "final_evaluation"]


class InputResultForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(InputResultForm, self).__init__(*args, **kwargs)
        self.fields['course'].choices = get_courses()
        self.fields['semester'].choices = get_semesters()
        self.fields['session'].choices = get_academic_sessions()

    course = forms.ChoiceField(choices=[])
    semester = forms.ChoiceField(choices=[])
    session = forms.ChoiceField(choices=[])
