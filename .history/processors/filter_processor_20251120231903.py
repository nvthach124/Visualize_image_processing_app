"""
Filter and Enhancement Processor

Handles blur operations, histogram equalization, and image enhancement.
"""

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from .base_processor import BaseProcessor


class FilterProcessor(BaseProcessor):
    """Processor for filtering and enhancement operations."""
    
    def equalized_image(self, image):
        """Apply histogram equalization to enhance contrast."""
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            equalized = cv2.equalizeHist(gray)
            code = "# Convert to grayscale and equalize histogram\n"
            code += "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
            code += "result = cv2.equalizeHist(gray)\n"
            return equalized, code
        else:
            try:
                equalized = cv2.equalizeHist(image)
                code = "# Equalize histogram\nresult = cv2.equalizeHist(image)\n"
                return equalized, code
            except Exception:
                messagebox.showerror("Error", "Failed to equalize histogram. Image format not supported.")
                return None

    def gaussian_blur_dialog(self, image):
        """Apply Gaussian blur with adjustable kernel size."""
        result = None
        dialog, main_frame, canvas, controls, buttons, result_ref = self._create_basic_preview_dialog("Gaussian Blur")
        
        k_size = tk.IntVar(value=5)
        
        ttk.Label(controls, text="Kernel Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        k_scale = ttk.Scale(controls, from_=1, to=51, variable=k_size, orient=tk.HORIZONTAL, length=300)
        k_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        k_label = ttk.Label(controls, text="5x5", width=5)
        k_label.grid(row=0, column=2, padx=5)
        
        controls.columnconfigure(1, weight=1)
        
        def update_preview(*args):
            k = k_size.get()
            if k % 2 == 0: k += 1
            k_label.config(text=f"{k}x{k}")
            
            try:
                blurred = cv2.GaussianBlur(image, (k, k), 0)
                self._update_preview_canvas(canvas, blurred, image)
            except Exception as e:
                canvas.delete("all")
                canvas.create_text(250, 150, text=str(e), fill="red")
        
        k_size.trace("w", update_preview)
        
        def apply_blur():
            k = k_size.get()
            if k % 2 == 0: k += 1
            blurred = cv2.GaussianBlur(image, (k, k), 0)
            code = f"# Apply Gaussian blur\nresult = cv2.GaussianBlur(image, ({k}, {k}), 0)\n"
            result_ref[0] = (blurred, code)
            dialog.destroy()
            
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons, text="Apply", command=apply_blur).pack(side=tk.RIGHT, padx=5)
        
        dialog.after(100, update_preview)
        dialog.wait_window()
        return result_ref[0]
        
    def median_blur_dialog(self, image):
        """Apply median blur for salt-and-pepper noise reduction."""
        result = None
        dialog, main_frame, canvas, controls, buttons, result_ref = self._create_basic_preview_dialog("Median Blur")
        
        k_size = tk.IntVar(value=5)
        
        ttk.Label(controls, text="Kernel Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        k_scale = ttk.Scale(controls, from_=1, to=51, variable=k_size, orient=tk.HORIZONTAL, length=300)
        k_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        k_label = ttk.Label(controls, text="5x5", width=5)
        k_label.grid(row=0, column=2, padx=5)
        
        controls.columnconfigure(1, weight=1)
        
        def update_preview(*args):
            k = k_size.get()
            if k % 2 == 0: k += 1
            k_label.config(text=f"{k}x{k}")
            
            try:
                blurred = cv2.medianBlur(image, k)
                self._update_preview_canvas(canvas, blurred, image)
            except Exception as e:
                canvas.delete("all")
                canvas.create_text(250, 150, text=str(e), fill="red")
        
        k_size.trace("w", update_preview)
        
        def apply_blur():
            k = k_size.get()
            if k % 2 == 0: k += 1
            blurred = cv2.medianBlur(image, k)
            code = f"# Apply median blur\nresult = cv2.medianBlur(image, {k})\n"
            result_ref[0] = (blurred, code)
            dialog.destroy()
            
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons, text="Apply", command=apply_blur).pack(side=tk.RIGHT, padx=5)
        
        dialog.after(100, update_preview)
        dialog.wait_window()
        return result_ref[0]
