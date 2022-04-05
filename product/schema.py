import graphene
from graphene_django import DjangoObjectType

from .models import Products, Reviews

class ProductsType(DjangoObjectType):
    class Meta:
        model = Products
        # fields = ("id", "name", "description", "image", "seller", "price", "review")

class ReviewsType(DjangoObjectType):
    class Meta:
        model = Reviews
        # fields = ("id", "text", "rating", "reviewer", "product")

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductsType)
    all_reviews = graphene.List(ReviewsType)

    def resolve_all_products(root, info):
        # We can easily optimize query count in the resolve method
        return Products.objects.all()

    def resolve_all_reviews(root, info):
        # We can easily optimize query count in the resolve method
        return Reviews.objects.all()

schema = graphene.Schema(query=Query)