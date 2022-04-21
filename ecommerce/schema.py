import graphene
from user.schema import Query as UserQuery, Mutation as UserMutation
from product.schema import (
    Query as ProductQuery,
    Mutation as ProductMutation,
)

class Query(UserQuery, ProductQuery):
    pass

class Mutation(UserMutation, ProductMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)