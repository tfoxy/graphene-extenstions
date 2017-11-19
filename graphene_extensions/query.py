import json
from typing import Dict

from graphql import Source, parse, validate, GraphQLSchema
from graphql.error import format_error, GraphQLSyntaxError
from graphql.execution import execute, ExecutionResult

from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest


class QueryExecutor:
    def __init__(self, schema):
        # type: (GraphQLSchema) -> None
        self.schema = schema
        assert isinstance(schema, GraphQLSchema), f'schema has to be of type GraphQLSchema, not {self.schema}'

    def query(self, query: str):
        # type: (str) -> dict
        result = self.execute_query(query)  # type: ExecutionResult
        if result.invalid:
            return {
                'errors': [self.format_error(error) for error in result.errors],
            }
        return {
            'data': result.data,
        }

    def execute_query(self, query):
        # type: (str) -> ExecutionResult
        source = Source(query)

        try:
            document_ast = parse(source=source)
        except GraphQLSyntaxError as e:
            return ExecutionResult(errors=[e], invalid=True)

        validation_errors = validate(self.schema, document_ast)
        if validation_errors:
            return ExecutionResult(errors=validation_errors, invalid=True)
        return execute(self.schema, document_ast)

    @classmethod
    def format_error(cls, error):
        # type: (Exception) -> Dict[str]
        if isinstance(error, GraphQLSyntaxError):
            return format_error(error)
        return {'message': str(error)}


def get_query_from_raw_json(data):
    # type: (str) -> str
    try:
        json_query = json.loads(data)
    except (ValueError, TypeError) as e:
        raise ValueError(e.message)

    if not isinstance(json_query, dict):
        raise ValueError('The received data is not a valid JSON query.')

    if 'query' not in json_query:
        raise ValueError('"query" not in request json')
    return json_query['query']


def get_query_from_request(request):
    # type: (WSGIRequest) -> str

    if request.GET.get('query'):
        return request.GET['query']
    if request.content_type in ('text/plain',):
        return ''

    if request.content_type == 'application/graphql':
        return request.body.decode()
    elif request.content_type == 'application/json':
        try:
            return get_query_from_raw_json(request.body.decode('utf-8'))
        except ValueError as e:
            raise ValidationError(str(e))
    elif request.content_type in ('application/x-www-form-urlencoded', 'multipart/form-data'):
        return request.POST
    else:
        raise ValidationError(f'Unsupported content-type {request.content_type}')

