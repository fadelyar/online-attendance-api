import graphene
import graphql_jwt
from graphene import String, ObjectType, Mutation, Field
from graphene_django import DjangoObjectType
from .models import User
from utils import json_parser
from graphene_file_upload.scalars import Upload


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserNewType(DjangoObjectType):
    class Meta:
        model = User


class UserMutateType(DjangoObjectType):
    class Meta:
        model = User


class CreateUser(Mutation):
    class Arguments:
        name = String(required=True)
        email = String(required=True)
        password = String(required=True)

    user = Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = User(name=name, email=email, password=password)
        user.save()
        return CreateUser(user=user)


class UpdateProfilePicture(Mutation):
    class Arguments:
        user_id = String(required=True)
        profile = String(required=True)

    user = Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user_id = kwargs.get('user_id')
        profile = kwargs.get('profile')
        if info.context.user.is_authenticated and user_id == info.context.user.id:
            user = User.objects.get(pk=user_id)
            user.profile_picture = profile
            user.save()
            return UpdateProfilePicture(user=user)
        raise ValueError('unauthorized user action!')


class DeleteUser(Mutation):
    class Arguments:
        user_id = String(required=True)

    user = Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user_id = kwargs.get('user_id')
        if info.context.user.is_authenticated and info.context.user.is_admin:
            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                return DeleteUser(user=user)
            except User.DoesNotExist:
                raise ValueError('user does Not exist with the given id!')


class UpdateUser(Mutation):
    class Arguments:
        user_id = String(required=True)
        first_name = String()
        last_name = String()
        email = String()
        about_me = String()

    user = Field(UserMutateType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            user_id = kwargs.get('user_id', None)
            user = User.objects.get(pk=user_id)
            user.first_name = kwargs.get('first_name', user.first_name)
            user.last_name = kwargs.get('last_name', user.last_name)
            user.email = kwargs.get('email', user.email)
            user.about_me = kwargs.get('about_me', user.about_me)
            user.save()
            return UpdateUser(user=user)
        except User.DoesNotExist:
            raise ValueError('user with the specified id does not exist!')


def is_user_exist(user_name: str):
    try:
        user = User.objects.get(name=user_name)
        raise ValueError('user name already taken!')
    except User.DoesNotExist:
        return True


class RegisterUser(Mutation):
    class Arguments:
        name = String(required=True)
        password = String(required=True)
        # first_name = String()
        last_name = String()
        email = String()
        # about_me = String()

    user = Field(UserMutateType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user_name = kwargs.get('name').lower()
        is_user_exist(user_name)
        user = User()
        user.name = kwargs.get('name')
        user.set_password(kwargs.get('password'))
        # user.password = kwargs.get('password')
        user.last_name = kwargs.get('last_name', '')
        user.email = kwargs.get('email', '')
        user.save()
        return RegisterUser(user=user)


class UploadFile(Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, info, file, **kwargs):
        print(file)
        return UploadFile(success=True)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = Field(UserNewType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class UserMutations(ObjectType):
    # create_user = CreateUser
    # delete_user = DeleteUser
    update_user = UpdateUser.Field()
    # update_profile_picture = UpdateProfilePicture
    upload_file = UploadFile.Field()
    token_auth = ObtainJSONWebToken.Field()
    register_user = RegisterUser.Field()
