import graphene
from graphene import ObjectType, Field, List
from graphene_django import DjangoObjectType
from .models import ClassRoom, Student
from .util import WorkWithExcel, MONTH_DICTIONARY
from datetime import datetime


class ClassType(DjangoObjectType):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = '__all__'


class Query(ObjectType):
    get_classes_by_teacher = List(ClassType, teacher_name=graphene.NonNull(graphene.String))
    get_student_by_class = List(StudentType, class_name=graphene.NonNull(graphene.String))
    get_student_by_name = Field(
        StudentType,
        student_name=graphene.NonNull(graphene.String),
        path=graphene.String()
    )

    @staticmethod
    def resolve_get_student_by_name(root, info, **kwargs):
        student_name = kwargs.get('student_name')
        current_date = datetime.now()
        sheet_name = MONTH_DICTIONARY.get(f'{current_date.month}')
        path = kwargs.get('path', None)
        try:
            student = Student.objects.get(name=student_name)
            if path:
                ws = WorkWithExcel(path=path, sheet_name=str(sheet_name + '_sheet'))
                ws.take_attendance(
                    user_name=student.name.capitalize(),
                    father_name=student.name.capitalize()
                )
            return student
        except Student.DoesNotExist:
            raise ValueError('user does not exist')

    @staticmethod
    def resolve_get_classes_by_teacher(root, info, **kwargs):
        teacher_name = kwargs.get('teacher_name')
        try:
            return ClassRoom.objects.filter(teacher__user_name=teacher_name).all()
        except ClassRoom.DoesNotExist:
            raise ValueError('classes for the specified users does not exist!')

    @staticmethod
    def resolve_get_student_by_class(root, info, **kwargs):
        class_name = kwargs.get('class_name')
        try:
            return Student.objects.filter(classroom__class_name=class_name).all()
        except Student.DoesNotExist:
            raise ValueError('students does not exist!')
