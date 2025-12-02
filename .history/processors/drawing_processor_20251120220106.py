"""
Drawing Utilities Processor

Handles drawing lines, rectangles, circles, and text on images.
This imports the original implementations from process_monolithic_backup.py
"""

import sys
import os

# Add parent directory to Python path to import from backup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class DrawingProcessor:
    """Processor for drawing operations - wraps original implementation."""
    
    def __init__(self, Image=None, ImageTk=None):
        """Initialize with PIL dependencies."""
        # Create instance of monolithic class with same PIL deps
        self._monolithic = MonolithicFP(Image, ImageTk)
    
    def draw_Line(self, image):
        """Draw lines on image - delegates to original implementation."""
        return self._monolithic.draw_Line(image)
    
    def draw_Rectangle(self, image):
        """Draw rectangles on image - delegates to original implementation."""
        return self._monolithic.draw_Rectangle(image)
    
    def draw_Circle(self, image):
        """Draw circles on image - delegates to original implementation."""
        return self._monolithic.draw_Circle(image)
    
    def draw_text(self, image):
        """Add text to image - delegates to original implementation."""
        return self._monolithic.draw_text(image)

