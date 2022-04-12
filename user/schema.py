import graphene
from graphene_django import DjangoObjectType


from .models import Seller

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

# class VerifyAccount(
#     MutationMixin, DynamicArgsMixin, VerifyAccountMixin, graphene.Mutation
# ):
#     __doc__ = VerifyAccountMixin.__doc__
#     _required_args = ["token"]

#     def sendWelcomeEmail():


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field() # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()







class SellerType(DjangoObjectType):
    class Meta:
        model = Seller
        # fields = ('id', 'shop_name', 'full_name', 'phone_number', 'email')


class CreateSellerMutation(graphene.Mutation):
    class Arguments:
        shop_name = graphene.String()
        full_name = graphene.String()
        phone_number = graphene.String()
        email = graphene.String()
        password = graphene.String()

    seller = graphene.Field(SellerType)

    def mutate(root, info, password, shop_name, full_name, phone_number, email):
        seller = Seller(shop_name=shop_name, full_name=full_name, phone_number=phone_number, email=email)
        seller.set_password(password)
        seller.save()
        return CreateSellerMutation(seller=seller)


class UpdateSellerMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        shop_name = graphene.String()
        full_name = graphene.String()
        phone_number = graphene.String()

    seller = graphene.Field(SellerType)

    def mutate(root, info, id, shop_name, full_name, phone_number):
        seller = Seller.objects.get(id=id)
        if seller:
            seller.shop_name = shop_name
            seller.full_name = full_name
            seller.phone_number = phone_number
            seller.save()
            return UpdateSellerMutation(seller=seller)

class DeleteSellerMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    seller = graphene.Field(SellerType)

    def mutate(root, info,id):
        seller = Seller.objects.get(id=id)
        if seller:
            seller.delete()
            return 




class Query(UserQuery, MeQuery, graphene.ObjectType):
    
    all_sellers = graphene.List(SellerType)

    def resolve_all_sellers(root, info):
        # We can easily optimize query count in the resolve method
        return Seller.objects.all() 


class Mutation(AuthMutation, CreateSellerMutation, UpdateSellerMutation, DeleteSellerMutation, graphene.ObjectType):
    create_seller = CreateSellerMutation.Field(description="Create new user")
    update_seller = UpdateSellerMutation.Field(description="Update exisiting user")
    delete_seller = DeleteSellerMutation.Field(description="Delete a user")
    # pass


schema = graphene.Schema(query=Query, mutation=Mutation)