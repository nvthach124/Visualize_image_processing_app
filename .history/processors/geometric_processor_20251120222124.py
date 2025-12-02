"""
Geometric Transformation Processor

Handles resize, flip, rotate, move, and perspective transformations.
This imports the original implementations from process_monolithic_backup.py
"""

import sys
import os
import cv2

# Add parent directory to Python path to import from backup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class GeometricProcessor:
    """Processor for geometric transformations - wraps original implementation."""
    
    def __init__(self, Image=None, ImageTk=None):
        """Initialize with PIL dependencies."""
        # Create instance of monolithic class with same PIL deps
        self._monolithic = MonolithicFP(Image, ImageTk)
    
    # Quick operations (no dialog)
    def rotate_image(self, image):
        """Rotate image by 90 degrees clockwise."""
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE), "cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)\n"
    
    def flip_Horizontal_image(self, image):
        """Flip image horizontally."""
        return cv2.flip(image, 1), "cv2.flip(image, 1)  # Horizontal flip\n"
    
    def flip_Vertical_image(self, image):
        """Flip image vertically."""
        return cv2.flip(image, 0), "cv2.flip(image, 0)  # Vertical flip\n"
    
    # Dialog operations - delegate to original
    def resize_image(self, image):
        """Resize image with custom dimensions - delegates to original."""
        return self._monolithic.resize_image(image)
    
    def flip_image(self, image):
        """Flip image with dialog - delegates to original."""
        return self._monolithic.flip_image(image)
    
    def rotationMatrix2d(self, image):
        """Apply custom rotation - delegates to original."""
        return self._monolithic.rotationMatrix2d(image)
    
    def move_image(self, image):
        """Translate/move image - delegates to original."""
        return self._monolithic.move_image(image)
    
    def perspectiveTransform(self, image):
        """Apply perspective transformation - delegates to original."""
        return self._monolithic.perspectiveTransform(image)

