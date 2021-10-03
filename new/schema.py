import graphene
from  accounts import schema
import accounts
from  location import schema
import location

class Query(accounts.schema.Query, location.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project    
    pass


class Mutation(accounts.schema.Mutation, location.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)