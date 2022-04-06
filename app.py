import user_profile.schema
import attendance.schema
import graphene


class RootQuery(user_profile.schema.Query, attendance.schema.Query, graphene.ObjectType):
    pass


class RootMutation(user_profile.schema.UserMutations, attendance.schema.AttendanceMutation):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
