"""
Intensity Transformation Processor

Handles contrast enhancement, log transform, power transform, and histogram operations.
This imports the original implementations from process_monolithic_backup.py
"""

import sys
import os

# Add parent directory to Python path to import from backup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class IntensityProcessor:
    """Processor for intensity transformations - wraps original implementation."""
    
    def __init__(self, Image=None, ImageTk=None):
        """Initialize with PIL dependencies."""
        # Create instance of monolithic class with same PIL deps
        self._monolithic = MonolithicFP(Image, ImageTk)
    
    def histogram_calculation(self, image):
        """Calculate and display histogram - delegates to original implementation."""
        return self._monolithic.histogram_calculation(image)
    
    def contrast_enhancement_dialog(self, image):
        """Enhance image contrast - delegates to original implementation."""
        return self._monolithic.contrast_enhancement_dialog(image)
        def contrast_enhancement_dialog(self, image):

    def log_transform_dialog(self, image):
        """Apply logarithmic transformation - delegates to original implementation."""
        return self._monolithic.log_transform_dialog(image)
    
    def power_transform_dialog(self, image):
        """Apply power-law (gamma) transformation - delegates to original implementation."""
        return self._monolithic.power_transform_dialog(image)
