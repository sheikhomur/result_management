import pdfkit, os
from django.template.loader import render_to_string
from django.conf import settings
import zipfile


def get_pdfkit_configuration():
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    return config


def generate_grade_sheets(student, results_dict):
    configuration = get_pdfkit_configuration()
    file_paths = []

    for semester in results_dict:

        # calculate total credit, total gpa, and total letter grade
        total_credit = 0
        total_gpa = 0
        for item in results_dict[semester]:
            total_credit += item.course.credit
            total_gpa += item.gpa * item.course.credit
        try:
            total_cgpa = round(total_gpa / total_credit, 2)
        except ZeroDivisionError:
            total_cgpa = 0.00

        letter_grade = "A+" if total_cgpa >= 4 else "A" if total_cgpa >= 3.75 else "A-" if total_cgpa >= 3.50\
                    else "B+" if total_cgpa >= 3.25 else "B" if total_cgpa >= 3.00 else "B-" if total_cgpa >= 2.75\
                    else "C+" if total_cgpa >= 2.50 else "C" if total_cgpa >= 2.25 else "C-" if total_cgpa >= 2.00\
                    else "F"

        context = {
            "student": student,
            "results": results_dict[semester],
            "semester": semester,
            "total_credit": total_credit,
            "total_cgpa": total_cgpa,
            "letter_grade": letter_grade,
        }

        string = render_to_string('result/grade-sheet.html', context)
        filename = f"{student.registration_number}__{semester.code}.pdf"
        filepath = os.path.join(settings.BASE_DIR, 'mediafiles', filename)
        pdfkit.from_string(string,
            filepath,
            options={"enable-local-file-access": ""},
            configuration=configuration)
        file_paths.append(filepath)
    return file_paths


def create_zip_file(filename, file_paths):
    filename = os.path.join(settings.BASE_DIR, 'mediafiles', f'{filename}.zip')
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            zipf.write(file,  os.path.relpath(file, os.path.join(file, '..')))
    
    return filename
