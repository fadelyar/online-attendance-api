from .attendance_query import Query
from .attendance_mutations import AttendanceMutation
from graphene import Schema

schema = Schema(query=Query, mutation=AttendanceMutation)
