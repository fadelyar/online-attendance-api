from graphene import String, ObjectType, Field, List
from graphene_django import DjangoObjectType
from .models import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ['id', 'user_name', 'email', 'profile_picture', 'auth_token']


class Query(ObjectType):
    get_user_by_email = Field(UserType, email=String())

    @staticmethod
    def resolve_get_user_by_email(root, info, **kwargs):
        email = kwargs.get('email', None)
        try:
            return Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            raise ValueError('user with the given id does not exist!')
