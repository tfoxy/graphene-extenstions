import pytest

import graphene


@pytest.fixture(scope='session')
def empty_schema():
    class Query(graphene.ObjectType):
        data = graphene.Field(type=graphene.String)

        def resolve_data(self, info) -> str:
            return 'dummy data'
    return graphene.Schema(query=Query)
