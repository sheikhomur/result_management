# Generated by Django 3.2 on 2023-01-16 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0007_semester_exam_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='department.academicsession'),
        ),
    ]
