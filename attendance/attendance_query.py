import graphene
from graphene import ObjectType, Field, List
from graphene_django import DjangoObjectType
from .models import ClassRoom, Student
from .util import WorkWithSpreadSheet, MONTH_DICTIONARY
from datetime import datetime
from user_profile.models import Profile


class ClassType(DjangoObjectType):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = '__all__'


class Query(ObjectType):
    get_classes_by_teacher = List(ClassType, teacher_email=graphene.NonNull(graphene.String))
    get_student_by_class = List(StudentType, class_id=graphene.NonNull(graphene.String))
    take_student_attendance = Field(
        StudentType,
        student_name=graphene.NonNull(graphene.String),
        class_name=graphene.NonNull(graphene.String),
        teacher_email=graphene.NonNull(graphene.String),
        token=graphene.NonNull(graphene.String)
    )

    @staticmethod
    def resolve_take_student_attendance(root, info, **kwargs):
        student_name = kwargs.get('student_name')
        class_name = kwargs.get('class_name')
        current_date = datetime.now()
        teacher_email = kwargs.get('teacher_email')
        sheet_name = MONTH_DICTIONARY.get(f'{current_date.month}')
        try:
            student = Student.objects.get(name=student_name)
            teacher = Profile.objects.get(email=teacher_email)
            ws = WorkWithSpreadSheet(
                title=class_name,
                work_sheet=MONTH_DICTIONARY.get(f'{sheet_name}'),
                user_name=student.name,
                father_name=student.father_name,
                token=teacher.auth_token,
                teacher_email=teacher_email
            )
            ws.take_attendance()
            return student

        except Student.DoesNotExist:
            raise ValueError('user does not exist')

    @staticmethod
    def resolve_get_classes_by_teacher(root, info, **kwargs):
        teacher_email = kwargs.get('teacher_email')
        try:
            return ClassRoom.objects.filter(teacher__email=teacher_email).all()
        except ClassRoom.DoesNotExist:
            raise ValueError('classes for the specified users does not exist!')

    @staticmethod
    def resolve_get_student_by_class(root, info, **kwargs):
        class_name = kwargs.get('class_id')
        try:
            return Student.objects.filter(classroom__id=class_name).all()
        except Student.DoesNotExist:
            raise ValueError('students does not exist!')
