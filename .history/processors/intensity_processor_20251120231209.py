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
        """Apply logarithmic transformation to enhance dark regions."""
        result = None
        dialog = tk.Toplevel()
        dialog.title("Log Transform")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Variables
        c_value = tk.DoubleVar(value=1.0)

        # Preview
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(preview_frame, text="Original:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(preview_frame, text="Log Transform:").grid(row=0, column=1, padx=5, pady=5)

        orig_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        orig_canvas.grid(row=1, column=0, padx=10, pady=5)

        result_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        result_canvas.grid(row=1, column=1, padx=10, pady=5)

        # Controls
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(controls_frame, text="Log Transform Formula: s = c * log(1 + r)").pack(pady=10)
        ttk.Label(controls_frame, text="Constant c:").pack(anchor=tk.W, pady=5)
        c_scale = ttk.Scale(controls_frame, from_=0.1, to=5.0, variable=c_value, orient=tk.HORIZONTAL, length=400)
        c_scale.pack(fill=tk.X, pady=5)
        ttk.Label(controls_frame, textvariable=c_value).pack(pady=5)

        def update_preview(*args):
            c = c_value.get()
            normalized = image.astype(np.float32) / 255.0
            log_img = c * np.log1p(normalized)
            log_img = np.clip(log_img * 255, 0, 255).astype(np.uint8)
            
            self._update_preview_canvas(orig_canvas, image, image)
            self._update_preview_canvas(result_canvas, log_img, image)

        def apply_log():
            nonlocal result
            c = c_value.get()
            normalized = image.astype(np.float32) / 255.0
            log_img = c * np.log1p(normalized)
            log_img = np.clip(log_img * 255, 0, 255).astype(np.uint8)
            
            code = f"# Log transformation\n"
            code += f"import numpy as np\n"
            code += f"c = {c:.2f}\n"
            code += f"normalized = image.astype(np.float32) / 255.0\n"
            code += f"log_img = c * np.log1p(normalized)\n"
            code += f"result = np.clip(log_img * 255, 0, 255).astype(np.uint8)\n"
            
            result = (log_img, code)
            dialog.destroy()

        c_value.trace("w", update_preview)

        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_log).pack(side=tk.RIGHT, padx=5)

        update_preview()
        dialog.wait_window()
        return result

    def power_transform_dialog(self, image):
        """Apply power-law (gamma) transformation."""
        result = None
        dialog = tk.Toplevel()
        dialog.title("Power Transform (Gamma Correction)")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Variables
        gamma = tk.DoubleVar(value=1.0)
        c_value = tk.DoubleVar(value=1.0)

        # Preview
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(preview_frame, text="Original:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(preview_frame, text="Power Transform:").grid(row=0, column=1, padx=5, pady=5)

        orig_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        orig_canvas.grid(row=1, column=0, padx=10, pady=5)

        result_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        result_canvas.grid(row=1, column=1, padx=10, pady=5)

        # Controls
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(controls_frame, text="Power Transform Formula: s = c * r^γ").pack(pady=10)
        
        ttk.Label(controls_frame, text="Gamma (γ): < 1 brightens, > 1 darkens").pack(anchor=tk.W, pady=5)
        gamma_scale = ttk.Scale(controls_frame, from_=0.1, to=5.0, variable=gamma, orient=tk.HORIZONTAL, length=400)
        gamma_scale.pack(fill=tk.X, pady=5)
        ttk.Label(controls_frame, textvariable=gamma).pack(pady=5)

        ttk.Label(controls_frame, text="Constant c:").pack(anchor=tk.W, pady=5)
        c_scale = ttk.Scale(controls_frame, from_=0.1, to=2.0, variable=c_value, orient=tk.HORIZONTAL, length=400)
        c_scale.pack(fill=tk.X, pady=5)
        ttk.Label(controls_frame, textvariable=c_value).pack(pady=5)

        def update_preview(*args):
            g = gamma.get()
            c = c_value.get()
            normalized = image.astype(np.float32) / 255.0
            power_img = c * np.power(normalized, g)
            power_img = np.clip(power_img * 255, 0, 255).astype(np.uint8)
            
            self._update_preview_canvas(orig_canvas, image, image)
            self._update_preview_canvas(result_canvas, power_img, image)

        def apply_power():
            nonlocal result
            g = gamma.get()
            c = c_value.get()
            normalized = image.astype(np.float32) / 255.0
            power_img = c * np.power(normalized, g)
            power_img = np.clip(power_img * 255, 0, 255).astype(np.uint8)
            
            code = f"# Power-law (gamma) transformation\n"
            code += f"import numpy as np\n"
            code += f"gamma = {g:.2f}\n"
            code += f"c = {c:.2f}\n"
            code += f"normalized = image.astype(np.float32) / 255.0\n"
            code += f"power_img = c * np.power(normalized, gamma)\n"
            code += f"result = np.clip(power_img * 255, 0, 255).astype(np.uint8)\n"
            
            result = (power_img, code)
            dialog.destroy()

        gamma.trace("w", update_preview)
        c_value.trace("w", update_preview)

        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_power).pack(side=tk.RIGHT, padx=5)

        update_preview()
        dialog.wait_window()
        return result
