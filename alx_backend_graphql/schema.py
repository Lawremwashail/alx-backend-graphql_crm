import graphene
from crm.schema import CRMQuery  # import from crm app

class Query(CRMQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)

