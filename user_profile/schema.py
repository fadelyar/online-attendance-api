from .user_query import Query
from .user_mutations import UserMutations
from graphene import Schema

schema = Schema(query=Query, mutation=UserMutations)
