"""
Base Processor Module

Contains base class and helper functions shared across all processors.
"""

import cv2
import tkinter as tk
from tkinter import ttk
import numpy as np


class BaseProcessor:
    """
    Base class for all image processors.
    Provides common helper functions and PIL dependency injection.
    """
    
    def __init__(self, pil_image_module, pil_image_tk_module):
        """
        Initialize with PIL modules via dependency injection.
        
        Args:
            pil_image_module: PIL.Image module
            pil_image_tk_module: PIL.ImageTk module
        """
        self.Image = pil_image_module
        self.ImageTk = pil_image_tk_module
    
    def _create_basic_preview_dialog(self, title, geometry="700x500"):
        """
        Create a standard preview dialog with canvas and control buttons.
        
        Args:
            title: Dialog window title
            geometry: Window size in format "WIDTHxHEIGHT"
            
        Returns:
            tuple: (dialog, main_frame, preview_canvas, controls_frame, buttons_frame, result_var)
        """
        result = [None]
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.geometry(geometry)
        dialog.resizable(False, False)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text=title, font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview canvas
        preview_frame = ttk.LabelFrame(main_frame, text="Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        preview_canvas = tk.Canvas(preview_frame, width=650, height=300, bg="lightgray")
        preview_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        return dialog, main_frame, preview_canvas, controls_frame, buttons_frame, result
    
    def _update_preview_canvas(self, canvas, image, original_image):
        """
        Update preview canvas with processed image.
        
        Args:
            canvas: tkinter Canvas widget
            image: Processed image to display
            original_image: Original image for size reference
        """
        h, w = original_image.shape[:2]
        canvas_w = canvas.winfo_width() if canvas.winfo_width() > 1 else 650
        canvas_h = canvas.winfo_height() if canvas.winfo_height() > 1 else 300
        
        scale = min(canvas_w / w, canvas_h / h, 1.0)
        display_w, display_h = int(w * scale), int(h * scale)
        
        resized = cv2.resize(image, (display_w, display_h))
        
        if len(resized.shape) == 2:
            rgb = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
        else:
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        pil_img = self.Image.fromarray(rgb)
        photo = self.ImageTk.PhotoImage(pil_img)
        
        canvas.delete("all")
        canvas.create_image(canvas_w // 2, canvas_h // 2, anchor='center', image=photo)
        canvas.image = photo
