import graphene
from .models import ClassRoom, Student
from .attendance_query import ClassType, StudentType
from user_profile.models import Profile


class CreateClass(graphene.Mutation):
    class Arguments:
        class_name = graphene.String(required=True)
        teacher_id = graphene.String(required=True)

    class_room = graphene.Field(ClassType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        class_name = kwargs.get('class_name')
        teacher_id = kwargs.get('teacher_id')
        try:
            teacher = Profile.objects.get(pk=teacher_id)
        except Profile.DoesNotExist:
            raise ValueError('teacher with specified name does not exist')
        new_class = ClassRoom()
        new_class.class_name = class_name
        new_class.teacher = teacher
        new_class.save()
        return CreateClass(class_room=new_class)


class CreateStudent(graphene.Mutation):
    class Arguments:
        class_id = graphene.String(required=True)
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        profile_picture = graphene.String()

    student = graphene.Field(StudentType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        class_id = kwargs.get('class_id')
        student_name = kwargs.get('name')
        student_email = kwargs.get('email')
        profile_picture = kwargs.get('profile_picture')
        new_student = Student()
        class_room = ClassRoom.objects.get(pk=class_id)
        try:
            new_student = Student.objects.get(email=student_email)
            class_room.students.add(new_student)
        except Student.DoesNotExist:
            new_student = Student()
            new_student.name = student_name
            new_student.email = student_email
            new_student.profile_picture = profile_picture
            new_student.save()
            class_room.students.add(new_student)
        return CreateStudent(student=new_student)


class DeleteClass(graphene.Mutation):
    class Arguments:
        class_id = graphene.String(required=True)

    class_room = graphene.Field(ClassType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        class_id = kwargs.get('class_id')
        deleted_class = ClassRoom.objects.get(pk=class_id).delete()
        return DeleteClass(class_room=deleted_class)


class DeleteStudent(graphene.Mutation):
    class Arguments:
        student_id = graphene.String(required=True)

    student = graphene.Field(StudentType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        student_id = kwargs.get('student_id')
        deleted_student = Student.objects.get(pk=student_id)
        return DeleteStudent(student=deleted_student)


class AttendanceMutation(graphene.ObjectType):
    create_class = CreateClass.Field()
    delete_class = DeleteClass.Field()
    create_student = CreateStudent.Field()
    delete_student = DeleteStudent.Field()
