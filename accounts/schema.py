from django.db.models import fields
from graphene import relay, ObjectType
import graphene
from graphene.types import interface
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import MyUser , Otp
import graphql_jwt

class MyuserNode(DjangoObjectType):
    class Meta:
        model = MyUser
        filter_fields = ['email', 'username', 'id']
        interfaces = (relay.Node, )

class MyUserInput(graphene.InputObjectType):
    phone_number = graphene.String()
    password = graphene.String()
    id = graphene.ID()


class MyUserUpdateMutation(graphene.Mutation):
    class Input:
        input = MyUserInput()

    myuser = graphene.Field(MyuserNode)


    @classmethod
    def mutate(cls, root, info, input):
        myuser = MyUser.objects.get(pk=input.id)
        if input.phone_number:
            myuser.phone_number = input.phone_number
        
        if input.password:
            myuser.set_password(input.password)
            
        myuser.save()

        return MyUserUpdateMutation(myuser=myuser)


class OtpNode(DjangoObjectType):
    class Meta:
        model = Otp
        filter_fields = ['code', 'id']
        interfaces = (relay.Node, )

class OtpInput(graphene.InputObjectType):
    user_id = graphene.ID()
    code = graphene.String()


class OtpUpdateMutation(graphene.Mutation):
    class Input:
        input = OtpInput()
    
    # otp = graphene.Field(OtpNode)
     
    status = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        status =False
        otp = Otp.objects.filter(user_id=input.user_id).last()
        if input.code == otp.code :
            otp.is_verify = True
            otp.user.is_verify = True
            otp.save()
            otp.user.save()
            status = True
        return  OtpUpdateMutation(status=status)



class Query(graphene.ObjectType):
    user = relay.Node.Field(MyuserNode)
    all_users = DjangoFilterConnectionField(MyuserNode)

    otp = relay.Node.Field(OtpNode)
    all_otps = DjangoFilterConnectionField(OtpNode)



class Mutation(graphene.ObjectType):
    update_myuser = MyUserUpdateMutation.Field()

    update_otp = OtpUpdateMutation.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()



