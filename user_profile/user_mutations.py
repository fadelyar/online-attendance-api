from graphene import String, ObjectType, Mutation, Field
from graphene_django import DjangoObjectType
from .models import Profile


class UserRegisterType(DjangoObjectType):
    class Meta:
        model = Profile


class UserDeleteType(DjangoObjectType):
    class Meta:
        model = Profile


class RegisterUser(Mutation):
    class Arguments:
        user_name = String(required=True)
        password = String(required=True)
        email = String()

    user = Field(UserRegisterType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        email = kwargs.get('email')
        try:
            Profile.objects.get(email=email)
            raise ValueError('email already taken')
        except Profile.DoesNotExist:
            user = Profile()
            user.user_name = kwargs.get('user_name')
            user.set_password(kwargs.get('password'))
            user.email = kwargs.get('email')
            user.save()
            return RegisterUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        email = String(required=True)

    user = Field(UserDeleteType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        email = kwargs.get('email')
        user = Profile.objects.get(email=email)
        user.delete()
        return DeleteUser(user)


class UserMutations(ObjectType):
    register_user = RegisterUser.Field()
    delete_user = DeleteUser.Field()
