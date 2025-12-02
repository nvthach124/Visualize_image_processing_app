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
    def _create_basic_preview_dialog(self, title, geometry="700x500"):
        """Helper function to create basic preview dialog structure.
        
        Args:
            title: Dialog window title
            geometry: Window size as "WxH" string
            
        Returns:
            Tuple of (dialog, main_frame, preview_frame, controls_frame, buttons_frame)
        """
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.geometry(geometry)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=title, font=("Arial", 14, "bold")).pack(pady=5)
        
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        preview_canvas = tk.Canvas(preview_frame, bg="lightgray", bd=1, relief=tk.SOLID)
        preview_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        return dialog, preview_canvas, controls_frame, buttons_frame

    def morph_operations_dialog(self, image):
        """Apply morphological operations: erode, dilate, open, close"""
        result = None
        dialog, canvas, controls, buttons = self._create_basic_preview_dialog("Morphological Operations", "700x600")
        
        op_type = tk.IntVar(value=cv2.MORPH_ERODE)
        k_size = tk.IntVar(value=5)
        iterations = tk.IntVar(value=1)
        
        # Controls
        # Operation Type
        op_frame = ttk.LabelFrame(controls, text="Operation Type")
        op_frame.pack(fill=tk.X, pady=5)
        
        ops = [
            ("Erode", cv2.MORPH_ERODE),
            ("Dilate", cv2.MORPH_DILATE),
            ("Open", cv2.MORPH_OPEN),
            ("Close", cv2.MORPH_CLOSE),
        ]
        
        for text, val in ops:
            ttk.Radiobutton(op_frame, text=text, variable=op_type, value=val).pack(side=tk.LEFT, padx=10, pady=5)
            
        # Kernel Size
        k_frame = ttk.Frame(controls)
        k_frame.pack(fill=tk.X, pady=5)
        ttk.Label(k_frame, text="Kernel Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        k_scale = ttk.Scale(k_frame, from_=1, to=51, variable=k_size, orient=tk.HORIZONTAL, length=300)
        k_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        k_label = ttk.Label(k_frame, text="5x5", width=5)
        k_label.grid(row=0, column=2, padx=5)
        k_frame.columnconfigure(1, weight=1)
        
        # Iterations
        iter_frame = ttk.Frame(controls)
        iter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(iter_frame, text="Iterations:").grid(row=0, column=0, sticky=tk.W, padx=5)
        iter_scale = ttk.Scale(iter_frame, from_=1, to=10, variable=iterations, orient=tk.HORIZONTAL, length=300)
        iter_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        iter_label = ttk.Label(iter_frame, textvariable=iterations, width=5)
        iter_label.grid(row=0, column=2, padx=5)
        iter_frame.columnconfigure(1, weight=1)
        
        def update_preview(*args):
            k = k_size.get()
            if k % 2 == 0: k += 1
            k_label.config(text=f"{k}x{k}")
            
            kernel = np.ones((k, k), np.uint8)
            op = op_type.get()
            iters = iterations.get()
            
            try:
                morphed = cv2.morphologyEx(image, op, kernel, iterations=iters)
                self._update_preview_canvas(canvas, morphed, image)
            except Exception as e:
                canvas.delete("all")
                canvas.create_text(250, 150, text=str(e), fill="red")
        
        op_type.trace("w", update_preview)
        k_size.trace("w", update_preview)
        iterations.trace("w", update_preview)
        
        def apply_morph():
            nonlocal result
            k = k_size.get()
            if k % 2 == 0: k += 1
            kernel = np.ones((k, k), np.uint8)
            op = op_type.get()
            iters = iterations.get()
            
            morphed = cv2.morphologyEx(image, op, kernel, iterations=iters)
            
            op_name = next(name for name, val in ops if val == op)
            op_code = f"cv2.MORPH_{op_name.upper()}"
            
            code = f"kernel = np.ones(({k}, {k}), np.uint8)\n"
            code += f"morphed = cv2.morphologyEx(image, {op_code}, kernel, iterations={iters})\n"
            
            result = (morphed, code)
            dialog.destroy()
            
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons, text="Apply", command=apply_morph).pack(side=tk.RIGHT, padx=5)
        
        dialog.after(100, update_preview) # Cập nhật preview ban đầu
        dialog.wait_window()
        return result
