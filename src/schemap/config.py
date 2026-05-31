from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any

@dataclass
class SchemaConfig:
    """ Configuration for auto-generated schemas """

    # Fields to exclude from specific schemas
    exclude_always : List[str] = field(default_factory=list)
    exclude_create : List[str] = field(default_factory=list)
    exclude_update : List[str] = field(default_factory=list)
    exclude_public : List[str] = field(default_factory=list)

    # Override field types or add validation
    field_overrides : Dict[str, Any] = field(default_factory=dict)

    # Force required/optional
    required_always : List[str] = field(default_factory=list)
    optional_always : List[str] = field(default_factory=list)

    # Custom validators to attach
    extra_validators : Dict[str, Callable] = field(default_factory=dict)