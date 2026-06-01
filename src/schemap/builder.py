from typing import Type, Any, Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import inspect
from pydantic import create_model, ConfigDict, field_validator

from .types import extract_column_metadata
from .utils.schema import should_include, transform_for_schema


def build_schema(
    model: Type[DeclarativeBase],
    schema_type: str = "default",  # "default", "create", "update", "public"
    config: Optional[Any] = None,  # SchemaConfig
) -> Any:
    """
    Build a Pydantic schema class for a SQLAlchemy model.
    
    Args:
        model: The SQLAlchemy model class (e.g., User)
        schema_type: Which schema variant to build
        config: Optional SchemaConfig for customization
        
    Returns:
        A Pydantic model class
    """
    
    inspector = inspect(model)

    columns_meta = []

    for col in inspector.columns:
        meta = extract_column_metadata(col)
        if should_include(schema_type, meta, config):
            columns_meta.append(meta)

    fields = {}
    
    for col_meta in columns_meta:
        field_type, field_kwargs = transform_for_schema(col_meta, schema_type, config)
        fields[col_meta["name"]] = (field_type, field_kwargs)

    schema_name = f"{model.__name__}{schema_type.capitalize()}Schema"

    validators = {}
    if config and config.extra_validators:
        for field_name, validator_func in config.extra_validators.items():
            # Wrap the validator with field_validator BEFORE passing to create_model
            validators[f"validate_{field_name}"] = field_validator(field_name)(validator_func)

    # Create model with validators built-in
    schema_class = create_model(
        schema_name,
        __config__=ConfigDict(from_attributes=True),
        __validators__=validators or None,
        **fields,
    )
    return schema_class