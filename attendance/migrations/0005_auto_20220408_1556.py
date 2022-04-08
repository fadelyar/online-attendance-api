# Generated by Django 3.2.8 on 2022-04-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_classroom_excel_sheet_path_student_father_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='excel_sheet_path',
        ),
        migrations.AddField(
            model_name='classroom',
            name='short_description',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
    ]
