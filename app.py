# import user_profile.schema
# import team_players.schema
# import graphene
#
#
# class RootQuery(user_profile.schema.Query, team_players.schema.Query, graphene.ObjectType):
#     pass
#
#
# class RootMutation(user_profile.schema.UserMutations):
#     pass
#
#
# schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
