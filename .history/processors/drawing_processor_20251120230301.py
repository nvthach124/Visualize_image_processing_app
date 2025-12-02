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
    
   

