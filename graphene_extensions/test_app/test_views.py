from django.http.response import HttpResponse
from django.test.client import RequestFactory

from graphene_extensions.status import STATUS_200_OK, STATUS_400_BAD_REQUEST
from graphene_extensions.views import GraphQLView

from .schema import schema


def test_empty_query(rf: RequestFactory):
    for request in (rf.get('graphql', data={}), rf.post('graphql', data={})):
        response: HttpResponse = GraphQLView.as_view(schema=schema)(request)
        assert response.status_code == STATUS_400_BAD_REQUEST, str(response.content)
        assert b'Syntax Error GraphQL' in response.content and b'Unexpected EOF' in response.content
