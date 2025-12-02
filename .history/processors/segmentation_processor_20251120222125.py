"""
Segmentation and Edge Detection Processor

Handles thresholding and edge detection operations.
"""

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from .base_processor import BaseProcessor


class SegmentationProcessor(BaseProcessor):
    """Processor for segmentation and edge detection."""
    
    def adaptive_threshold_dialog(self, image):
        """Apply adaptive thresholding with interactive preview."""
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        result = None
        dialog, main_frame, canvas, controls, buttons, result_ref = self._create_basic_preview_dialog(
            "Adaptive Threshold", "800x600"
        )
        
        method_var = tk.IntVar(value=cv2.ADAPTIVE_THRESH_MEAN_C)
        thresh_type = tk.IntVar(value=cv2.THRESH_BINARY)
        block_size = tk.IntVar(value=11)
        c_value = tk.IntVar(value=2)
        
        # Method selection
        method_frame = ttk.LabelFrame(controls, text="Adaptive Method")
        method_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(method_frame, text="Mean", variable=method_var, 
                       value=cv2.ADAPTIVE_THRESH_MEAN_C).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(method_frame, text="Gaussian", variable=method_var,
                       value=cv2.ADAPTIVE_THRESH_GAUSSIAN_C).pack(side=tk.LEFT, padx=10)
        
        # Threshold type
        type_frame = ttk.LabelFrame(controls, text="Threshold Type")
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(type_frame, text="Binary", variable=thresh_type,
                       value=cv2.THRESH_BINARY).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Binary Inverted", variable=thresh_type,
                       value=cv2.THRESH_BINARY_INV).pack(side=tk.LEFT, padx=10)
        
        # Block size
        block_frame = ttk.Frame(controls)
        block_frame.pack(fill=tk.X, pady=5)
        ttk.Label(block_frame, text="Block Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        block_scale = ttk.Scale(block_frame, from_=3, to=51, variable=block_size, orient=tk.HORIZONTAL, length=300)
        block_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Label(block_frame, textvariable=block_size).grid(row=0, column=2, padx=5)
        block_frame.columnconfigure(1, weight=1)
        
        # C value
        c_frame = ttk.Frame(controls)
        c_frame.pack(fill=tk.X, pady=5)
        ttk.Label(c_frame, text="C Value:").grid(row=0, column=0, sticky=tk.W, padx=5)
        c_scale = ttk.Scale(c_frame, from_=-50, to=50, variable=c_value, orient=tk.HORIZONTAL, length=300)
        c_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Label(c_frame, textvariable=c_value).grid(row=0, column=2, padx=5)
        c_frame.columnconfigure(1, weight=1)
        
        def update_preview(*args):
            bs = block_size.get()
            if bs % 2 == 0: bs += 1
            c = c_value.get()
            method = method_var.get()
            thresh_t = thresh_type.get()
            
            try:
                thresh = cv2.adaptiveThreshold(gray, 255, method, thresh_t, bs, c)
                self._update_preview_canvas(canvas, thresh, image)
            except Exception as e:
                canvas.delete("all")
                canvas.create_text(250, 150, text=str(e), fill="red")
        
        method_var.trace("w", update_preview)
        thresh_type.trace("w", update_preview)
        block_size.trace("w", update_preview)
        c_value.trace("w", update_preview)
        
        def apply_threshold():
            bs = block_size.get()
            if bs % 2 == 0: bs += 1
            c = c_value.get()
            method = method_var.get()
            thresh_t = thresh_type.get()
            
            if len(image.shape) > 2 and image.shape[2] > 1:
                gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                conversion = "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
            else:
                gray_img = image
                conversion = ""
            
            thresh = cv2.adaptiveThreshold(gray_img, 255, method, thresh_t, bs, c)
            
            method_name = "ADAPTIVE_THRESH_MEAN_C" if method == cv2.ADAPTIVE_THRESH_MEAN_C else "ADAPTIVE_THRESH_GAUSSIAN_C"
            thresh_name = "THRESH_BINARY" if thresh_t == cv2.THRESH_BINARY else "THRESH_BINARY_INV"
            
            code = "# Adaptive thresholding\n" + conversion
            code += f"result = cv2.adaptiveThreshold(gray, 255, cv2.{method_name}, cv2.{thresh_name}, {bs}, {c})\n"
            
            result_ref[0] = (thresh, code)
            dialog.destroy()
        
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons, text="Apply", command=apply_threshold).pack(side=tk.RIGHT, padx=5)
        
        dialog.after(100, update_preview)
        dialog.wait_window()
        return result_ref[0]
