import json
from typing import Tuple, Union

from graphql import parse, validate, Source
from graphql.error import format_error, GraphQLSyntaxError
from graphql.execution import execute, ExecutionResult
from graphql.type.schema import GraphQLSchema

from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest

from .status import STATUS_200_OK, STATUS_400_BAD_REQUEST


class GraphQLView(View):
    graphiql_version = '0.11.10'
    graphiql_template = 'graphiql.html'

    schema = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert isinstance(self.get_schema(), GraphQLSchema), \
            f'schema has to be of type GraphQLSchema, not {self.schema}'

    def dispatch(self, request, *args, **kwargs):
        if request.method not in ('GET', 'POST'):
            return HttpResponseNotAllowed(['GET', 'POST'], 'GraphQL only supports GET and POST requests.')

        if self.show_graphiql:
            return self.render_graphiql()

        try:
            return self.get_graphql_response()
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)

    def render_graphiql(self):
        result, status_code = self.get_query_result()
        context = self.get_context_data()
        context.update({'result': self.jsonify(result)})
        return render(self.request, self.graphiql_template, context=context, status=status_code)

    def get_graphql_response(self):
        result, status_code = self.get_query_result()
        return HttpResponse(content=self.jsonify(result), status=status_code, content_type='application/json')

    def get_query_result(self):
        # type: () -> Tuple[Union[dict, None], int]
        result = self.execute_query()  # type: ExecutionResult
        if not result:
            return {}, STATUS_400_BAD_REQUEST
        if result.invalid:
            return {
                'errors': [self.format_error(error) for error in result.errors],
            }, STATUS_400_BAD_REQUEST
        return {
            'data': result.data,
        }, STATUS_200_OK

    @classmethod
    def jsonify(cls, data: dict):
        if settings.DEBUG:
            return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        return json.dumps(data, separators=(',', ':'))

    @classmethod
    def format_error(cls, error):
        if isinstance(error, GraphQLSyntaxError):
            return format_error(error)
        return {'message': str(error)}

    @classmethod
    def parse_json_body(cls, data):
        try:
            json_query = json.loads(data)
        except (ValueError, TypeError) as e:
            raise ValidationError(e.message)

        if not isinstance(json_query, dict):
            raise ValidationError('The received data is not a valid JSON query.')

        if 'query' not in json_query:
            raise ValidationError('"query" not in request json')
        return json_query['query']

    def get_raw_query(self):
        # type: () -> dict
        if self.request.GET.get('query'):
            return self.request.GET['query']
        if self.request.content_type in ('text/plain',):
            return {}

        if self.request.content_type == 'application/graphql':
            return self.request.body.decode()
        elif self.request.content_type == 'application/json':
            return self.parse_json_body(self.request.body.decode('utf-8'))
        elif self.request.content_type in ('application/x-www-form-urlencoded', 'multipart/form-data'):
            return self.request.POST
        else:
            raise ValidationError(f'Unsupported content-type {self.request.content_type}')

    def execute_query(self):
        raw_query = self.get_raw_query()
        if not raw_query:
            return ExecutionResult()
        source = Source(raw_query)

        try:
            document_ast = parse(source=source)
        except GraphQLSyntaxError as e:
            return ExecutionResult(errors=[e], invalid=True)

        validation_errors = validate(self.get_schema(), document_ast)
        if validation_errors:
            return ExecutionResult(errors=validation_errors, invalid=True)
        return execute(self.get_schema(), document_ast)

    def get_schema(self):
        return self.schema

    @property
    def show_graphiql(self):
        return settings.DEBUG and self.request.content_type in ('text/plain',)

    def get_context_data(self):
        return {
            'title': 'GraphiQL',
            'graphiql_version': self.graphiql_version,
            'query': self.get_raw_query(),
        }
