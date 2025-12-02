"""
Morphological Operations Processor

Handles erosion, dilation, opening, and closing operations.
"""

import cv2
import tkinter as tk
from tkinter import ttk
import numpy as np
from .base_processor import BaseProcessor


class MorphologyProcessor(BaseProcessor):
    """Processor for morphological operations."""
    
    
