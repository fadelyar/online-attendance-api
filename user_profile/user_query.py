from graphene import String, ObjectType, Field, List
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_admin', 'first_name', 'last_name']


class Query(ObjectType):
    users = List(UserType)
    get_user_by_id = Field(UserType, id=String())

    @staticmethod
    def resolve_users(root, info):
        # user = info.context.user
        # if user.is_authenticated and user.is_admin:
        return User.objects.all()
        # raise ValueError('authorization error!')

    @staticmethod
    def resolve_get_user_by_id(root, info, **kwargs):
        user_id = kwargs.get('id', None)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValueError('user with the given id does not exist!')
