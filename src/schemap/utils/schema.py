from typing import Any, Optional, Annotated
from pydantic import Field

def should_include(schema_type: str, metadata: dict[str, Any], config: Optional[Any] = None):
    """Determine if a column should be included in the schema."""

    if config is not None:
        if metadata["name"] in config.exclude_always:
            return False
        if schema_type == "public" and metadata["name"] in config.exclude_public:
            return False
        if schema_type == "create" and metadata["name"] in config.exclude_create:
            return False
        if schema_type == "update" and metadata["name"] in config.exclude_update:
            return False

    if schema_type == "default":
        return True
    
    elif schema_type == "create":

        # Exclude primary keys and server_default fields
        if metadata["primary_key"]:
            return False
        
        if metadata.get("server_default") is not None:
            return False
        
        if metadata.get("default") is not None:
            return False
        
        return True
    
    elif schema_type == "update":
        
        # Exclude primary keys only
        if metadata["primary_key"]:
            return False
        
        return True
    
    elif schema_type == "public":
        
        # Exclude fields starting with __ (private)
        if metadata["name"].startswith("__"):
            return False
        
        return True
    
    else:
        raise ValueError(f"Unknown schema_type: {schema_type}")
    
def transform_for_schema(metadata: dict, schema_type: str, config: Optional[Any]) -> tuple[type, Any]:
    """Transform column metadata into (field_type, Field(...)) for create_model."""
    
    field_name = metadata["name"]
    
    config_defaults = _get_config_defaults(config, field_name)
    
    type_info = _resolve_type_and_nullability(metadata, config_defaults)
    
    field_def = _apply_schema_rules(type_info, schema_type)
    
    field_def = _apply_validators(field_def, config, field_name)
    
    return field_def


def _get_config_defaults(config: Optional[Any], field_name: str) -> dict:
    """Extract config defaults or provide empty fallbacks."""
    if config is None:
        return {
            "override_type": None,
            "is_required_forced": False,
            "is_optional_forced": False,
            "has_validator": False
        }
    
    return {
        "override_type": config.field_overrides.get(field_name),
        "is_required_forced": field_name in config.required_always,
        "is_optional_forced": field_name in config.optional_always,
        "has_validator": field_name in config.extra_validators
    }


def _resolve_type_and_nullability(metadata: dict, config_defaults: dict) -> dict:
    """Determine final Python type and whether field is optional."""
    field_name = metadata["name"]
    base_type = config_defaults["override_type"] or metadata["python_type"]
    
    # Forced overrides take precedence
    if config_defaults["is_required_forced"]:
        is_optional = False
        has_default = False
        default_value = None
    elif config_defaults["is_optional_forced"]:
        is_optional = True
        has_default = True
        default_value = None
    else:
        is_optional = metadata["is_optional"]
        has_default = metadata.get("default") is not None
        default_value = metadata.get("default")
    
    return {
        "name": field_name,
        "base_type": base_type,
        "is_optional": is_optional,
        "has_default": has_default,
        "default_value": default_value,
        "max_length": metadata.get("max_length")
    }


def _apply_schema_rules(type_info: dict, schema_type: str) -> tuple[type, Any]:
    """Apply schema-specific rules (update/create/default)."""
    base_type = type_info["base_type"]
    is_optional = type_info["is_optional"]
    has_default = type_info["has_default"]
    default_value = type_info["default_value"]
    
    # Build Field kwargs from constraints
    field_kwargs = {}
    if type_info["max_length"] is not None:
        field_kwargs["max_length"] = type_info["max_length"]
    
    # Update schema: all fields Optional with None default
    if schema_type == "update":
        field_kwargs["default"] = None
        return (Optional[base_type], Field(**field_kwargs) if field_kwargs else ...)
    
    # Create schema: respect metadata, exclude server_default fields already filtered
    elif schema_type == "create":
        if has_default:
            field_kwargs["default"] = default_value
            return (base_type, Field(**field_kwargs) if field_kwargs else ...)
        elif is_optional:
            field_kwargs["default"] = None
            return (Optional[base_type], Field(**field_kwargs) if field_kwargs else ...)
        else:
            return (base_type, Field(**field_kwargs) if field_kwargs else ...)
    
    # Default or Public schema
    else:
        if has_default:
            field_kwargs["default"] = default_value
            return (base_type, Field(**field_kwargs) if field_kwargs else ...)
        elif is_optional:
            field_kwargs["default"] = None
            return (Optional[base_type], Field(**field_kwargs) if field_kwargs else ...)
        else:
            return (base_type, Field(**field_kwargs) if field_kwargs else ...)


def _apply_validators(field_def: tuple[type, Any], config: Optional[Any], field_name: str) -> tuple[type, Any]:
    """Wrap field type with Annotated if custom validator exists."""
    if not config or field_name not in config.extra_validators:
        return field_def
    
    field_type, field_args = field_def
    validator = config.extra_validators[field_name]
    
    # Wrap the type with Annotated[original_type, validator]
    annotated_type = Annotated[field_type, validator]
    
    return (annotated_type, field_args)