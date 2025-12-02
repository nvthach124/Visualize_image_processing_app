"""
Image Processing - REFACTORED VERSION
3328 lines -> 200 lines modular
"""

from processors.color_processor import ColorProcessor
from processors.geometric_processor import GeometricProcessor  
from processors.filter_processor import FilterProcessor
from processors.segmentation_processor import SegmentationProcessor
from processors.morphology_processor import MorphologyProcessor
from processors.intensity_processor import IntensityProcessor
from processors.advanced_processor import AdvancedProcessor
from processors.drawing_processor import DrawingProcessor


class FunctionsProcessing:
    """Main facade class - delegates to processors"""
    
    def __init__(self, Image=None, ImageTk=None):
        self.Image = Image
        self.ImageTk = ImageTk
        self.color_proc = ColorProcessor(Image, ImageTk)
        self.geometric_proc = GeometricProcessor(Image, ImageTk)
        self.filter_proc = FilterProcessor(Image, ImageTk)
        self.segmentation_proc = SegmentationProcessor(Image, ImageTk)
        self.morphology_proc = MorphologyProcessor(Image, ImageTk)
        self.intensity_proc = IntensityProcessor(Image, ImageTk)
        self.advanced_proc = AdvancedProcessor(Image, ImageTk)
        self.drawing_proc = DrawingProcessor(Image, ImageTk)
        
    # Color conversions
    def cvt_Negative(self, image):
        return self.color_proc.cvt_Negative(image)
    def cvt_HSV(self, image):
        return self.color_proc.cvt_HSV(image)
    def cvt_GRAY(self, image):
        return self.color_proc.cvt_GRAY(image)
    
    # Geometric
    def rotate_image(self, image):
        return self.geometric_proc.rotate_image(image)
    def resize_image(self, image):
        return self.geometric_proc.resize_image(image)
    def flip_image(self, image):
        return self.geometric_proc.flip_image(image)
    def flip_Horizontal_image(self, image):
        return self.geometric_proc.flip_Horizontal_image(image)
    def flip_Vertical_image(self, image):
        return self.geometric_proc.flip_Vertical_image(image)
    def rotationMatrix2d(self, image):
        return self.geometric_proc.rotationMatrix2d(image)
    def move_image(self, image):
        return self.geometric_proc.move_image(image)
    def perspectiveTransform(self, image):
        return self.geometric_proc.perspectiveTransform(image)
    
    # Filters
    def equalized_image(self, image):
        return self.filter_proc.equalized_image(image)
    def gaussian_blur_dialog(self, image):
        return self.filter_proc.gaussian_blur_dialog(image)
    def median_blur_dialog(self, image):
        return self.filter_proc.median_blur_dialog(image)
    def bilateral_filter_dialog(self, image):
        return self.filter_proc.bilateral_filter_dialog(image)
    def canny_detection(self, image):
        return self.filter_proc.canny_detection(image)
    
    # Segmentation
    def binary_threshold_dialog(self, image):
        return self.segmentation_proc.binary_threshold_dialog(image)
    def adaptive_threshold_dialog(self, image):
        return self.segmentation_proc.adaptive_threshold_dialog(image)
    def otsu_threshold(self, image):
        return self.segmentation_proc.otsu_threshold(image)
    
    # Morphology
    def morphology_dialog(self, image):
        return self.morphology_proc.morph_operations_dialog(image)
    
    # Intensity
    def histogram_calculation(self, image):
        return self.intensity_proc.histogram_calculation(image)
    def contrast_enhancement_dialog(self, image):
        return self.intensity_proc.contrast_enhancement_dialog(image)
    def log_transform_dialog(self, image):
        return self.intensity_proc.log_transform_dialog(image)
    def power_transform_dialog(self, image):
        return self.intensity_proc.power_transform_dialog(image)
    
    # Advanced
    def image_registration_dialog(self, image):
        return self.advanced_proc.image_registration_dialog(image)
    def image_stitching_dialog(self, image):
        return self.advanced_proc.image_stitching_dialog(image)
    
    # Drawing
    def draw_Line(self, image):
        return self.drawing_proc.draw_Line(image)
    def draw_Rectangle(self, image):
        return self.drawing_proc.draw_Rectangle(image)
    def draw_Circle(self, image):
        return self.drawing_proc.draw_Circle(image)
    def draw_text(self, image):
        return self.drawing_proc.draw_text(image)
