from graphene import String, ObjectType, Field, List
from graphene_django import DjangoObjectType
from .models import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ['id', 'user_name', 'email', 'profile_picture']


class Query(ObjectType):
    get_user_by_id = Field(UserType, id=String())

    @staticmethod
    def resolve_get_user_by_id(root, info, **kwargs):
        user_id = kwargs.get('id', None)
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            raise ValueError('user with the given id does not exist!')
