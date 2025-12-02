"""
Color Space Conversion Processor

Handles color space transformations like RGB, HSV, Grayscale, and Negative.
"""

import cv2
from .base_processor import BaseProcessor


class ColorProcessor(BaseProcessor):
    """Processor for color space conversions."""
    
    def cvt_Negative(self, image):
        """
        Convert to Negative image color space.
        
        Args:
            image: Input image
            
        Returns:
            tuple: (processed_image, code_string)
        """
        result = cv2.bitwise_not(image)
        code = "# Convert to negative\nresult = cv2.bitwise_not(image)\n"
        return result, code

    def cvt_HSV(self, image):
        """
        Convert BGR to HSV color space.
        
        Args:
            image: Input BGR image
            
        Returns:
            tuple: (hsv_image, code_string)
        """
        result = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        code = "# Convert BGR to HSV\nresult = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)\n"
        return result, code

    def cvt_GRAY(self, image):
        """
        Convert BGR to Grayscale.
        
        Args:
            image: Input BGR image
            
        Returns:
            tuple: (gray_image, code_string)
        """
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        code = "# Convert BGR to Grayscale\nresult = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
        return result, code
