from django.contrib import admin
from .models import Result


class ResultAdmin(admin.ModelAdmin):
    list_display = [
        "course", "semester", "session", "student",
        "tt_mark", "attendance", "final_evaluation",
    ]
    list_filter =['course', 'session', 'semester']

admin.site.register(Result, ResultAdmin)
