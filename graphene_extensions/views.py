import json
from collections import OrderedDict
from typing import Tuple, Union

from django.core.handlers.wsgi import WSGIRequest

from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest

from .query import get_query_from_request, QueryExecutor
from .status import STATUS_200_OK, STATUS_400_BAD_REQUEST


class GraphQLView(View):
    allowed_methods = ('GET', 'POST')

    graphiql_version = '0.11.10'  # type: str
    graphiql_template = 'graphiql.html'  # type: str

    schema = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query_executor = QueryExecutor(self.schema)

    def dispatch(self, request, *args, **kwargs):
        # type: (WSGIRequest) -> HttpResponse
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
            return render(self.request, self.graphiql_template, context=context, status=status_code)

        return HttpResponse(content=result, status=status_code, content_type='application/json')

    def get_query(self):
        # type: () -> str
        return get_query_from_request(self.request)

    def get_query_result(self, query):
        # type: (str) -> Tuple[Union[str, None], int]
        result = self.query_executor.query(query)
        return self.jsonify(result), STATUS_400_BAD_REQUEST if 'errors' in result else STATUS_200_OK

    @classmethod
    def jsonify(cls, data):
        # type: (dict) -> str
        if settings.DEBUG:
            return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        return json.dumps(data, separators=(',', ':'))

    def get_schema(self):
        return self.schema

    @property
    def show_graphiql(self):
        # type: () -> bool
        return settings.DEBUG and self.request.content_type in ('text/plain', 'text/html')

    def get_context_data(self):
        # type: () -> OrderedDict
        return OrderedDict({
            'title': 'GraphiQL',
            'graphiql_version': self.graphiql_version,
        })
