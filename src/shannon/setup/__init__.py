"""Shannon CLI setup and framework detection.

This module provides tools for:
- Detecting Shannon Framework installations
- Interactive setup wizard
- Framework verification and validation
- Auto-installation and bundling support

Exports:
    FrameworkDetector: Detect and verify Shannon Framework
    SetupWizard: Interactive installation guide
"""

from shannon.setup.framework_detector import FrameworkDetector
from shannon.setup.wizard import SetupWizard

__all__ = ['FrameworkDetector', 'SetupWizard']
