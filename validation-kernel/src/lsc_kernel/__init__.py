"""LSC Validation Kernel public API.

The package implements a specification and provenance gate.  It does not
contain a recovered numerical LSC model and it never substitutes historical
or illustrative coefficients for missing frozen values.
"""

__version__ = "0.6.0"

from .frozen.evaluator import FrozenLSCEvaluator
from .frozen.identity import FrozenModelIdentity
from .frozen.parameter_bundle import FrozenParameterBundle, validate_parameter_bundle
from .frozen.parameter_schema import FrozenParameterSchema

__all__ = [
    "FrozenLSCEvaluator",
    "FrozenModelIdentity",
    "FrozenParameterBundle",
    "FrozenParameterSchema",
    "validate_parameter_bundle",
]
