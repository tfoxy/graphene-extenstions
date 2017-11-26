# graphene-extenstions 

[![Build Status](https://travis-ci.org/karol-gruszczyk/graphene-extenstions.svg?branch=master)](https://travis-ci.org/karol-gruszczyk/graphene-extenstions)
[![Coverage Status](https://coveralls.io/repos/github/karol-gruszczyk/graphene-extenstions/badge.svg?branch=master)](https://coveralls.io/github/karol-gruszczyk/graphene-extenstions?branch=master)

Goal of this library is to make development on graphene a lot simpler and quicker,
 which means less boiler plate and more flexibility.

## Requirements
* Python 3.6+
* graphene 2.0+
* Django 1.10+

## Purpose
Why another library if there is already `graphene-django` available?
* Poor documentation, only a couple of documented features. v1 and v2 documentation is mixed,
 which ends up in user frustration.
 You can copy paste examples from the documentation and it will result in errors,
  because it's written for graphene v1, which is ridiculous.
* Lack of query optimization, which really should be handled by the framework itself
* Extendability is very poor.
 In most cases you need to copy-paste the source code into your project, to get more custom behaviour.
* But the main reason is, that the project is evolving very slowly and does not seem,
 that there will be any new features in the near future
* `django-rest-framework` dependency. Authors got really lazy and did not bother writing proper `Mutation` classes...
 Seriously, why do I need to install a REST library, when I want to use GraphQL?
* No Server Error handling, which results in Exception message leakage.

## Features
* Simple schema generation from django models
* Support for model properties and methods
* Query optimization, no more `prefetch_related` and `select_related`(sick!)
* [TODO] `Mutation` generation(with validators, similar to DRF style) from django models
* GraphiQL browser query executor

## Quick start

### Installation
`pip install graphene-extensions`

#### schema.py
```python
import graphene

from graphene_extensions.types import ModelType
from graphene_extensions.connections import ModelConnectionField
from graphene_extensions.types.decorators import annotate_type, graphene_property

from django.db import models


class Pizza(models.Model):
    name = models.CharField(max_length=128)
    
    @graphene_property(graphene.String)
    def custom_name(self):
        return f'Custom {self.name}'

    @annotate_type(graphene.String)
    def custom_method(self):
        return 'magic'


class PizzaType(ModelType):
    class Meta:
        model = Pizza
        fields = ('name', 'custom_name', 'custom_method')


class Query(graphene.ObjectType):
    pizzas = ModelConnectionField(PizzaType)

schema = graphene.Schema(query=Query)
```

#### urls.py
```python
from django.conf.urls import url

from graphene_extensions.views import GraphQLView

from .schema import schema

urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(schema=schema)),
]
```
