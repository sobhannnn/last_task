from django.db.models import fields
from graphene import relay, ObjectType, Connection, Node, Int
import graphene
from graphene.types import interface
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from accounts.models import MyUser
from .models import LocationUser
import graphql_jwt
import datetime
from datetime import datetime, date
import django_filters
from django_filters import FilterSet

class LocationUserFilter(django_filters.FilterSet):
    start = django_filters.DateRangeFilter(lookup_expr=['gte'])
    end = django_filters.DateRangeFilter(lookup_expr=['lte'])
    user = django_filters.CharFilter(lookup_expr=['iexact', 'istartswith', 'iendswith'])
    user_id = django_filters.CharFilter(lookup_expr=['exact'])
    locationuser_id = django_filters.CharFilter(lookup_expr=['exact'])
    class Meta:
        model = LocationUser
        fields = ['start', 'end', 'user', 'user_id', 'locationuser_id']

class LocationUserConnection(Connection):
    class Meta:
        abstract = True

    total_count = Int()
    edge_count = Int()
    total_hours = graphene.String()
    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)
    
    def resolve_total_hours(self, *_):
        all_nodes = self.iterable
        total_hours = 0 
        total_minute = 0
        for node in all_nodes:
            if node.end:
                calculated = str(node.end - node.start)
                calculated = calculated.split(":",)
                total_minute += int(calculated[1])
                total_hours += int(calculated[0])
        
        x = int(total_minute / 60)
        total_minute = total_minute - (x * 60)
        total_hours += x
        return f"{total_hours} : {total_minute}"

class LocationUserNode(DjangoObjectType):
    class Meta:
        model = LocationUser
        filterset_class = LocationUserFilter 
        interfaces = (relay.Node, )
        connection_class = LocationUserConnection
    
    calculated_field = graphene.String()

    def resolve_calculated_field(self,info,):
        if self.end:
            calculated = str(self.end - self.start)
            calculated = calculated.split(":",)
            return f"{calculated[0]} : {calculated[1]}"
        else:
            return "it's not finished"


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


