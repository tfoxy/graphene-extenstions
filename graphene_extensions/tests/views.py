import json

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.test.client import RequestFactory

from graphene_extensions.status import STATUS_200_OK, STATUS_400_BAD_REQUEST
from graphene_extensions.views import GraphQLView


def test_empty_query(rf: RequestFactory, empty_schema):
    for request in (rf.get('graphql', data={}), rf.post('graphql')):
        response: HttpResponse = GraphQLView.as_view(schema=empty_schema)(request)
        assert response.status_code == STATUS_400_BAD_REQUEST, str(response.content)
        assert b'Syntax Error GraphQL' in response.content and b'Unexpected EOF' in response.content


def test_valid_query(rf: RequestFactory, empty_schema):
    query = {'query': '''
    query {
      data
    }
    '''}
    for request in (rf.get('graphql', data=query), rf.post('graphql', data=query)):
        response: HttpResponse = GraphQLView.as_view(schema=empty_schema)(request)
        assert response.status_code == STATUS_200_OK, str(response.content)
        assert json.loads(response.content) == {'data': {'data': 'dummy data'}}


def test_invalid_query(rf: RequestFactory, empty_schema):
    query = {'query': '''
    query {
    }
    '''}
    for request in (rf.get('graphql', data=query), rf.post('graphql', data=query)):
        response: HttpResponse = GraphQLView.as_view(schema=empty_schema)(request)
        assert response.status_code == STATUS_400_BAD_REQUEST, str(response.content)
        assert 'errors' in json.loads(response.content)


def test_callable_schema(rf: RequestFactory, empty_schema):
    def get_schema(request: WSGIRequest):
        return empty_schema

    view = GraphQLView(schema=get_schema)
    view.request = rf.get('graphql', data={})
    assert view.get_schema() == empty_schema
