"""
Shannon Framework v4 - Specification Engine

Purpose: Parse, validate, and maintain project specifications with continuous
         adherence monitoring.

Components:
  - SpecificationParser: Converts user input to structured spec
  - SpecificationValidator: Schema and semantic validation
  - SpecificationMonitor: Real-time adherence checking
  - ConfidenceEvaluator: Integration with confidence-check skill

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .parser import SpecificationParser
from .validator import SpecificationValidator, ValidationError
from .monitor import SpecificationMonitor, SpecificationEvent, DeviationAlert, MonitoringContext
from .models import Specification, SpecificationObject

__all__ = [
    'SpecificationParser',
    'SpecificationValidator',
    'ValidationError',
    'SpecificationMonitor',
    'SpecificationEvent',
    'DeviationAlert',
    'MonitoringContext',
    'Specification',
    'SpecificationObject',
]

__version__ = '1.0.0'
