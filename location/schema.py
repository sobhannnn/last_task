from django.db.models import fields
from graphene import relay, ObjectType
import graphene
from graphene.types import interface
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from accounts.models import MyUser
from .models import LocationUser
import graphql_jwt
import datetime


class LocationUserNode(DjangoObjectType):
    class Meta:
        model = LocationUser
        filter_fields = ['id']
        interfaces = (relay.Node, )


class LocationUserInput(graphene.InputObjectType):
    location_lat = graphene.String()
    location_long = graphene.String()
    locationuser_id = graphene.ID()
    is_finished = graphene.Boolean()
    user_id = graphene.ID()


class LocationUserMutation(graphene.Mutation):
    class Input:
        input = LocationUserInput()

    locationuser = graphene.Field(LocationUserNode)


    @classmethod
    def mutate(cls, root, info, input):
        if input.locationuser_id:    
            locationuser = LocationUser.objects.filter(id = from_global_id(input.locationuser_id)[1]).last()
            locationuser.is_finished = True
            locationuser.end = datetime.datetime.now()
        
        if not input.locationuser_id:
            locationuser = LocationUser.objects.create(user_id = from_global_id(input.user_id)[1],
            start = datetime.datetime.now(), location_lat = input.location_lat, location_long = input.location_long)
                
            locationuser.is_finished = False
        
        locationuser.save()

        return LocationUserMutation(locationuser=locationuser)



            






class Query(graphene.ObjectType):
    locationuser = relay.Node.Field(LocationUserNode)
    all_locationusers = DjangoFilterConnectionField(LocationUserNode)


class Mutation(graphene.ObjectType):
    update_locationuser = LocationUserMutation.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


