"""
Main Processing Class - Aggregates all processors

This is the main interface that Gui.py will use. It combines all specialized
processors into a single class for backward compatibility.
"""

import cv2
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser, filedialog
import numpy as np

from .base_processor import BaseProcessor
from .color_processor import ColorProcessor
from .geometric_processor import GeometricProcessor


class FunctionsProcessing(BaseProcessor):
    """
    Main image processing class that aggregates all specialized processors.
    
    This class maintains backward compatibility while delegating work to
    specialized processor classes for better code organization.
    """
    
    def __init__(self, pil_image_module, pil_image_tk_module):
        """Initialize all processors."""
        super().__init__(pil_image_module, pil_image_tk_module)
        
        # Initialize specialized processors
        self.color_proc = ColorProcessor(pil_image_module, pil_image_tk_module)
        self.geom_proc = GeometricProcessor(pil_image_module, pil_image_tk_module)
    
    # ========================================================================
    # COLOR SPACE CONVERSIONS - Delegate to ColorProcessor
    # ========================================================================
    
    def cvt_Negative(self, image):
        """Convert to Negative image."""
        return self.color_proc.cvt_Negative(image)
    
    def cvt_HSV(self, image):
        """Convert BGR to HSV."""
        return self.color_proc.cvt_HSV(image)
    
    def cvt_GRAY(self, image):
        """Convert BGR to Grayscale."""
        return self.color_proc.cvt_GRAY(image)
    
    # ========================================================================
    # GEOMETRIC TRANSFORMATIONS - Delegate to GeometricProcessor
    # ========================================================================
    
    def rotate_image(self, image):
        """Rotate image by 90 degrees clockwise."""
        return self.geom_proc.rotate_image(image)
    
    def resize_image(self, image):
        """Resize image with custom dimensions or percentage."""
        return self.geom_proc.resize_image(image)
    
    def flip_image(self, image):
        """Flip image horizontally, vertically, or both."""
        return self.geom_proc.flip_image(image)
