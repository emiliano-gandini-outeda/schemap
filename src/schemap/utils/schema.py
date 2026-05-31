from typing import Any, Optional
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
    
    # Handle config being None
    if config is None:
        field_overrides = {}
        required_always = set()
        optional_always = set()
    else:
        field_overrides = config.field_overrides
        required_always = set(config.required_always)
        optional_always = set(config.optional_always)
    
    # Apply type override
    field_name = metadata["name"]
    python_type = field_overrides.get(field_name, metadata["python_type"])
    
    # Determine optional/required with forced overrides
    if field_name in required_always:
        is_optional = False
        has_default = False
        default_value = None
    elif field_name in optional_always:
        is_optional = True
        has_default = True
        default_value = None
    else:
        is_optional = metadata["is_optional"]
        has_default = metadata.get("default") is not None
        default_value = metadata.get("default")
    
    # Build Field kwargs from constraints
    field_kwargs = {}
    
    # String length constraint
    if metadata.get("max_length") is not None:
        field_kwargs["max_length"] = metadata["max_length"]
    
    # Update schema - all fields become Optional with None default
    if schema_type == "update":
        field_kwargs["default"] = None
        return (Optional[python_type], Field(**field_kwargs))
    
    # Create schema - exclude server_default fields already filtered
    elif schema_type == "create":
        if has_default:
            field_kwargs["default"] = default_value
            return (python_type, Field(**field_kwargs))
        elif is_optional:
            field_kwargs["default"] = None
            return (Optional[python_type], Field(**field_kwargs))
        else:
            # Required field with no default
            return (python_type, Field(**field_kwargs) if field_kwargs else ...)
    
    # Default or Public schema
    else:
        if has_default:
            field_kwargs["default"] = default_value
            return (python_type, Field(**field_kwargs))
        elif is_optional:
            field_kwargs["default"] = None
            return (Optional[python_type], Field(**field_kwargs))
        else:
            # Required field with no default
            return (python_type, Field(**field_kwargs) if field_kwargs else ...)