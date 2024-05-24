import os
from django.shortcuts import render
from django.views import View
from department.models import *
from result.forms import InputResultForm, StudentResultForm
from result.models import Result
from itertools import groupby
from django.contrib import messages
from django.http import FileResponse
from result.pdf_utils import create_zip_file, generate_grade_sheets


GRADE_DISTRIBUTION = {
    80: { "gpa": "4.00", "letter": "A+" },
    75: { "gpa": "3.75", "letter": "A" },
    70: { "gpa": "3.50", "letter": "A-" },
    65: { "gpa": "3.25", "letter": "B+" },
    60: { "gpa": "3.00", "letter": "B" },
    55: { "gpa": "2.75", "letter": "B-" },
    50: { "gpa": "2.50", "letter": "C+" },
    45: { "gpa": "2.25", "letter": "C" },
    40: { "gpa": "2.00", "letter": "C-" },
}


class DownloadStudentGradeSheetTemplate(View):

    def get(self, request, registration_number):
        student = Student.objects.filter(registration_number=registration_number).first()
        if not student:
            messages.warning(request, "No student found")

        results = Result.objects.filter(student=student).order_by("semester__code")

        results_dict = {}
        for semester_code, group in groupby(results, key=lambda x: x.semester):
            group = list(group)

            # for each of the result row, get it's semester and course, and total mark
            for result in group:
                total_mark = result.tt_mark + result.attendance + result.final_evaluation
                
                result.gpa = 4 if total_mark >= 80 else 3.75 if total_mark >= 75 else 3.50 if total_mark >= 70\
                    else 3.25 if total_mark >= 65 else 3 if total_mark >= 60 else 2.75 if total_mark >= 55\
                    else 2.50 if total_mark >= 50 else 2.25 if total_mark >= 45 else 2 if total_mark >= 40\
                    else 0
                
                result.letter_grade = "A+" if total_mark >= 80 else "A" if total_mark >= 75 else "A-" if total_mark >= 70\
                    else "B+" if total_mark >= 65 else "B" if total_mark >= 60 else "B-" if total_mark >= 55\
                    else "C+" if total_mark >= 50 else "C" if total_mark >= 45 else "C-" if total_mark >= 40\
                    else "F"
            
            semester_obj = Semester.objects.filter(code=semester_code).first()
            
            results_dict[semester_obj] = group

        gradesheet_paths = generate_grade_sheets(student, results_dict)
        zip_file = create_zip_file(registration_number, gradesheet_paths)

        # delete pdf files
        try:
            for file in gradesheet_paths:
                os.remove(file)
        except (FileNotFoundError, PermissionError, OSError):
            pass

        zip_file = open(zip_file, 'rb')
        return FileResponse(zip_file)


class StudentResultView(View):

    def get(self, request):
        form = StudentResultForm()
        context = {
            "form": form,
        }
        return render(request, 'result/student-result.html', context=context)
    
    def post(self, request):
        form = StudentResultForm(request.POST)

        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']
            
            student = Student.objects.filter(registration_number=registration_number).first()
            if not student:
                messages.warning(request, "No student found")

            results = Result.objects.filter(student=student).order_by("semester__code")


            results_dict = {}
            for semester_code, group in groupby(results, key=lambda x: x.semester):
                group = list(group)

                # for each of the result row, get it's semester and course, and total mark
                for result in group:
                    total_mark = result.tt_mark + result.attendance + result.final_evaluation
                    
                    result.gpa = 4 if total_mark >= 80 else 3.75 if total_mark >= 75 else 3.50 if total_mark >= 70\
                        else 3.25 if total_mark >= 65 else 3 if total_mark >= 60 else 2.75 if total_mark >= 55\
                        else 2.50 if total_mark >= 50 else 2.25 if total_mark >= 45 else 2 if total_mark >= 40\
                        else 0
                    
                    result.letter_grade = "A+" if total_mark >= 80 else "A" if total_mark >= 75 else "A-" if total_mark >= 70\
                        else "B+" if total_mark >= 65 else "B" if total_mark >= 60 else "B-" if total_mark >= 55\
                        else "C+" if total_mark >= 50 else "C" if total_mark >= 45 else "C-" if total_mark >= 40\
                        else "F"
                
                semester_obj = Semester.objects.filter(code=semester_code).first()
                
                results_dict[semester_obj] = group

            context = {
                "form": form,
                "student": student,
                "results_dict": results_dict
            }
        return render(request, 'result/student-result.html', context=context)


class InputResultView(View):

    template_name = "result/input-result.html"

    def get(self, request):
        search_result_form = InputResultForm()

        context = {
            'search_result_form': search_result_form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        search_result_form = InputResultForm(request.POST)

        context = {
            'search_result_form': search_result_form,
            "search_result": True
        }

        if search_result_form.is_valid():
            search_result_data = search_result_form.cleaned_data
            request_data = dict(request.POST)

            # get result
            semester = Semester.objects.filter(name=search_result_data["semester"]).first()
            session = AcademicSession.objects.filter(name=search_result_data["session"]).first()
            course = Course.objects.filter(name=search_result_data["course"]).first()
            
            # process result item (if it's a result submit request)
            if request_data.get('result_submit'):
                row_keys = list(filter(lambda x: x.startswith('row__'), request_data.keys()))
                # delete existing data
                Result.objects.filter(course=course, semester=semester, session=session).delete()
                for row in row_keys:
                    student, tt_mark, attendance, final_evaluation = request_data[row]
                    
                    # find the student
                    student_obj = Student.objects.filter(registration_number=student).first()
                    if not student_obj:
                        messages.warning(request, f"Invalid student's registration number: {student}")
                    else:
                        # save the results
                        Result.objects.create(
                            course=course,
                            semester=semester,
                            session=session,
                            student=student_obj,
                            tt_mark=tt_mark or 0,
                            attendance=attendance or 0,
                            final_evaluation=final_evaluation or 0,
                        )
                messages.success(request, "Result saved successfully!")

            results = Result.objects.filter(semester=semester, session=session, course=course)
            context['results'] = results
            return render(request, self.template_name, context=context)
        
        else:
            messages.warning(request, "Some error occurred, Please try again!")
            return render(request, self.template_name, context=context)


class TabulationSheetTemplate(View):

    def get(self, request, registration_number):
        
        student = Student.objects.filter(registration_number=registration_number).first()
        results = Result.objects.filter(student=student).order_by("semester__code")


        results_dict = {}
        for semester_code, group in groupby(results, key=lambda x: x.semester):
            group = list(group)

            # for each of the result row, get it's semester and course, and total mark
            for result in group:
                total_mark = result.tt_mark + result.attendance + result.final_evaluation
                
                result.gpa = 4 if total_mark >= 80 else 3.75 if total_mark >= 75 else 3.50 if total_mark >= 70\
                    else 3.25 if total_mark >= 65 else 3 if total_mark >= 60 else 2.75 if total_mark >= 55\
                    else 2.50 if total_mark >= 50 else 2.25 if total_mark >= 45 else 2 if total_mark >= 40\
                    else 0
                
                result.letter_grade = "A+" if total_mark >= 80 else "A" if total_mark >= 75 else "A-" if total_mark >= 70\
                    else "B+" if total_mark >= 65 else "B" if total_mark >= 60 else "B-" if total_mark >= 55\
                    else "C+" if total_mark >= 50 else "C" if total_mark >= 45 else "C-" if total_mark >= 40\
                    else "F"
            
            semester_obj = Semester.objects.filter(code=semester_code).first()
            
            results_dict[semester_obj] = group

        context = {
            "student": student,
            "results_dict": results_dict
        }
        return render(request, 'result/tabulation-sheet.html', context=context)
