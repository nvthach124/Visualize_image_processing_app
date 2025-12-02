"""
Intensity Transformation Processor

Handles contrast enhancement, log transform, power transform, and histogram operations.
This imports the original implementations from process_monolithic_backup.py
"""


import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from .base_processor import BaseProcessor

# Add parent directory to Python path to import from backup

# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class IntensityProcessor:
    """Processor for intensity transformations - wraps original implementation."""
    
    def __init__(self, Image=None, ImageTk=None):
        """Initialize with PIL dependencies."""
        # Create instance of monolithic class with same PIL deps
        self._monolithic = MonolithicFP(Image, ImageTk)
    
    def histogram_calculation(self, image):
        """Calculate and display histogram - delegates to original implementation."""
        return self._monolithic.histogram_calculation(image)

    def contrast_enhancement_dialog(self, image):
        """Enhance image contrast using various methods."""
        result = None
        dialog = tk.Toplevel()
        dialog.title("Contrast Enhancement")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Variables
        method_var = tk.StringVar(value="linear")
        alpha = tk.DoubleVar(value=1.5)  # Contrast control
        beta = tk.IntVar(value=0)  # Brightness control

        # Preview
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(preview_frame, text="Original:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(preview_frame, text="Enhanced:").grid(row=0, column=1, padx=5, pady=5)

        orig_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        orig_canvas.grid(row=1, column=0, padx=10, pady=5)

        result_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        result_canvas.grid(row=1, column=1, padx=10, pady=5)

        # Controls
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(controls_frame, text="Method:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(controls_frame, text="Linear", variable=method_var, value="linear").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(controls_frame, text="CLAHE", variable=method_var, value="clahe").grid(row=0, column=2, sticky=tk.W)

        ttk.Label(controls_frame, text="Contrast (α):").grid(row=1, column=0, sticky=tk.W, pady=5)
        alpha_scale = ttk.Scale(controls_frame, from_=0.1, to=3.0, variable=alpha, orient=tk.HORIZONTAL, length=300)
        alpha_scale.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=5)
        ttk.Label(controls_frame, textvariable=alpha, width=6).grid(row=1, column=3, padx=5)

        ttk.Label(controls_frame, text="Brightness (β):").grid(row=2, column=0, sticky=tk.W, pady=5)
        beta_scale = ttk.Scale(controls_frame, from_=-100, to=100, variable=beta, orient=tk.HORIZONTAL, length=300)
        beta_scale.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=5)
        ttk.Label(controls_frame, textvariable=beta, width=6).grid(row=2, column=3, padx=5)

        def update_preview(*args):
            if method_var.get() == "linear":
                enhanced = cv2.convertScaleAbs(image, alpha=alpha.get(), beta=beta.get())
            else:  # CLAHE
                if len(image.shape) == 2:
                    clahe = cv2.createCLAHE(clipLimit=alpha.get(), tileGridSize=(8, 8))
                    enhanced = clahe.apply(image)
                else:
                    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=alpha.get(), tileGridSize=(8, 8))
                    l = clahe.apply(l)
                    enhanced = cv2.merge([l, a, b])
                    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            
            self._update_preview_canvas(orig_canvas, image, image)
            self._update_preview_canvas(result_canvas, enhanced, image)

        def apply_contrast():
            nonlocal result
            if method_var.get() == "linear":
                enhanced = cv2.convertScaleAbs(image, alpha=alpha.get(), beta=beta.get())
                code = f"# Linear contrast enhancement\n"
                code += f"enhanced = cv2.convertScaleAbs(image, alpha={alpha.get():.2f}, beta={beta.get()})\n"
            else:
                if len(image.shape) == 2:
                    clahe = cv2.createCLAHE(clipLimit=alpha.get(), tileGridSize=(8, 8))
                    enhanced = clahe.apply(image)
                    code = f"# CLAHE enhancement\n"
                    code += f"clahe = cv2.createCLAHE(clipLimit={alpha.get():.2f}, tileGridSize=(8, 8))\n"
                    code += f"enhanced = clahe.apply(image)\n"
                else:
                    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=alpha.get(), tileGridSize=(8, 8))
                    l = clahe.apply(l)
                    enhanced = cv2.merge([l, a, b])
                    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
                    code = f"# CLAHE enhancement on LAB color space\n"
                    code += f"lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)\n"
                    code += f"l, a, b = cv2.split(lab)\n"
                    code += f"clahe = cv2.createCLAHE(clipLimit={alpha.get():.2f}, tileGridSize=(8, 8))\n"
                    code += f"l = clahe.apply(l)\n"
                    code += f"enhanced = cv2.merge([l, a, b])\n"
                    code += f"enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)\n"
            
            result = (enhanced, code)
            dialog.destroy()

        method_var.trace("w", update_preview)
        alpha.trace("w", update_preview)
        beta.trace("w", update_preview)

        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_contrast).pack(side=tk.RIGHT, padx=5)

        update_preview()
        dialog.wait_window()
        return result
    
    def log_transform_dialog(self, image):
        """Apply logarithmic transformation - delegates to original implementation."""
        return self._monolithic.log_transform_dialog(image)
    
    def power_transform_dialog(self, image):
        """Apply power-law (gamma) transformation - delegates to original implementation."""
        return self._monolithic.power_transform_dialog(image)
