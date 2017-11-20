import json
from collections import OrderedDict
from typing import Tuple, Union

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest

from graphql.type.schema import GraphQLSchema

from .query import get_query_from_request, QueryExecutor
from .status import STATUS_200_OK, STATUS_400_BAD_REQUEST


class GraphQLView(View):
    allowed_methods = ('GET', 'POST')

    graphiql_version: str = '0.11.10'
    graphiql_template: str = 'graphiql.html'

    schema: GraphQLSchema = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query_executor = QueryExecutor(self.schema)

    def dispatch(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if request.method not in self.allowed_methods:
            return HttpResponseNotAllowed(['GET', 'POST'], 'GraphQL only supports GET and POST requests.')

        try:
            query = self.get_query()
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)

        result, status_code = self.get_query_result(query)

        if self.show_graphiql:
            context = self.get_context_data()
            context.update({'result': result if query else '', 'query': query})
            return render(self.request, self.graphiql_template, context=context,
                          status=status_code if query else STATUS_200_OK)

        return HttpResponse(content=result, status=status_code, content_type='application/json')

    def get_query(self) -> str:
        return get_query_from_request(self.request)

    def get_query_result(self, query: str) -> Tuple[Union[str, None], int]:
        result = self.query_executor.query(query)
        return self.jsonify(result), STATUS_400_BAD_REQUEST if 'errors' in result else STATUS_200_OK

    @classmethod
    def jsonify(cls, data: dict) -> str:
        if settings.DEBUG:
            return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        return json.dumps(data, separators=(',', ':'))

    def get_schema(self):
        return self.schema

    @property
    def show_graphiql(self) -> bool:
        return settings.DEBUG and self.request.content_type in ('text/plain', 'text/html')

    def get_context_data(self) -> OrderedDict:
        return OrderedDict({
            'title': 'GraphiQL',
            'graphiql_version': self.graphiql_version,
        })
