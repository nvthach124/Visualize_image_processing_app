"""
Advanced Image Processing

Handles image registration and stitching operations.
This imports the original implementations from process_monolithic_backup.py
"""

import sys
import os

# Add parent directory to Python path to import from backup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class AdvancedProcessor:
    """Processor for advanced operations - wraps original implementation."""
    
    def __init__(self, Image=None, ImageTk=None):
        """Initialize with PIL dependencies."""
        # Create instance of monolithic class with same PIL deps
        self._monolithic = MonolithicFP(Image, ImageTk)
    
    def image_registration_dialog(self, image):
        """Register two images using feature matching - delegates to original."""
        return self._monolithic.image_registration_dialog(image)
    
    def image_stitching_dialog(self, image):
        """Stitch multiple images into panorama - delegates to original."""
        return self._monolithic.image_stitching_dialog(image)

