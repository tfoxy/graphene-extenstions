from typing import Type, List

from django.db.models import Model

from graphene.types.mutation import Mutation, MutationOptions


class ModelMutationOptions(MutationOptions):
    model: Type[Model] = None

    def __init__(self, model, fields, exclude_fields, class_type):
        super().__init__(class_type)
        self.model = model
        self.fields = self.resolve_fields(fields, exclude_fields)

    def resolve_fields(self, fields, exclude_fields):
        pass


class ModelMutation(Mutation):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, resolver=None, output=None, arguments=None, _meta=None,
                                    model=None, fields=None, exclude_fields=None,
                                    **options):
        if not _meta:
            _meta = ModelMutationOptions(model, class_type=cls)
        super().__init_subclass_with_meta__(resolver, output, arguments, _meta, **options)
