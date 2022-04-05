import graphene
from user.schema import Query as UserQuery, Mutation as UserMutation
from product.schema import Query as ProductQuery

class Query(UserQuery, ProductQuery):
    pass

class Mutation(UserMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)