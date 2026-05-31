"""Base classes for automatic schemap generation."""

from typing import Type, Any
from cached_classproperty import cached_classproperty
from sqlalchemy.orm import DeclarativeBase

from .builder import build_schema

class SchemaMixin:
    """ Mixin that ds auto-generated Pydantic schemas as class attributes """

    @cached_classproperty
    def Schema(cls) -> Any:
        """ Full schema with all columns """
        return build_schema(cls, schema_type="default")
    
    @cached_classproperty
    def CreateSchema(cls) -> Any:
        """ Schema for creating new instances (excludes primary keys, server defaults) """
        return build_schema(cls, schema_type="create")

    @cached_classproperty
    def UpdateSchema(cls) -> Any:
        """ Schema for partial updates (all fields optional) """
        return build_schema(cls, schema_type="update")
    
    @cached_classproperty
    def PublicSchema(cls) -> Any:
        """ Public-facing schema (excludes sensitive fields) """
        return build_schema(cls, schema_type="public")
    
    @classmethod
    def from_schema(cls, schema_obj : Any) -> Any:
        """ Create ORM instance from Pydantic Schema """
        return cls(**schema_obj.model_dump(exclude_none=True))

    def to_schema(self, schema_cls : Type[Any] = None) -> Any:
        """ Convert ORM instance to Pydantic schema """
        if schema_cls is None:
            schema_cls = self.Schema

        return schema_cls.model_validate(self)


class AutoBase(SchemaMixin, DeclarativeBase):
    """ Base class for all models. Inherit from this to get auto-schemas """
    pass