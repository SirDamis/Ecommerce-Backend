from email.mime import image
import graphene
from graphene_django import DjangoObjectType

from .models import Products, Reviews

from graphene_file_upload.scalars import Upload
from user.schema import SellerType, SellerInput

class ProductType(DjangoObjectType):
    class Meta:
        model = Products
        # fields = ("id", "name", "description", "image", "seller", "price", "review")

class CreateProductMutation(graphene.Mutation):


    class Arguments:
        name = graphene.String()
        description = graphene.String()
        image = Upload(required=True)
        seller = graphene.Argument(SellerInput)
        price = graphene.Float()

    product  = graphene.Field(ProductType)

    def mutate(root, info, name, description, image, seller, price):
        product = Products( name, description, image, seller, price)
        return CreateProductMutation(product=product)


class ReviewsType(DjangoObjectType):
    class Meta:
        model = Reviews
        # fields = ("id", "text", "rating", "reviewer", "product")

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    all_reviews = graphene.List(ReviewsType)

    def resolve_all_products(root, info):
        # We can easily optimize query count in the resolve method
        return Products.objects.all()

    def resolve_all_reviews(root, info):
        # We can easily optimize query count in the resolve method
        return Reviews.objects.all()

class Mutation(CreateProductMutation, graphene.ObjectType):
    create_product = CreateProductMutation.Field(description="Add new product")

schema = graphene.Schema(query=Query, mutation=Mutation)