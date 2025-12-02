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
    
    def canny_detection(self, image):
        """Detect edges using Canny edge detector with adjustable parameters."""
        # Create a copy of the image to preview
        img_copy = image.copy()
        
        result = None
        dialog = tk.Toplevel()
        dialog.title("Canny Edge Detection")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Frames
        top_frame = ttk.Frame(dialog)
        top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Variables
        threshold1 = tk.IntVar(value=100)  # Lower threshold
        threshold2 = tk.IntVar(value=200)  # Upper threshold
        aperture_size = tk.IntVar(value=3)  # Aperture size for Sobel
        l2gradient = tk.BooleanVar(value=False)  # L2 gradient
        
        # Title
        ttk.Label(top_frame, text="Canny Edge Detection", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(top_frame, text="Adjust parameters to detect edges in the image", font=("Arial", 10)).pack(pady=5)
        
        # Preview area
        preview_container = ttk.Frame(preview_frame)
        preview_container.pack(fill=tk.BOTH, expand=True)
        
        # Left preview (original)
        original_frame = ttk.LabelFrame(preview_container, text="Original Image")
        original_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Right preview (edge detection result)
        edge_frame = ttk.LabelFrame(preview_container, text="Edge Detection Result")
        edge_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        preview_container.columnconfigure(0, weight=1)
        preview_container.columnconfigure(1, weight=1)
        preview_container.rowconfigure(0, weight=1)
        
        # Canvas for image previews
        h, w = image.shape[:2]
        scale = min(350/w, 250/h)
        preview_w, preview_h = int(w*scale), int(h*scale)
        
        original_canvas = tk.Canvas(original_frame, width=preview_w, height=preview_h, bg="lightgray", bd=1, relief=tk.SOLID)
        original_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        edge_canvas = tk.Canvas(edge_frame, width=preview_w, height=preview_h, bg="lightgray", bd=1, relief=tk.SOLID)
        edge_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls
        controls_grid = ttk.Frame(controls_frame)
        controls_grid.pack(fill=tk.X, padx=5, pady=5)
        

    
        
        # Threshold 1 (lower)
        ttk.Label(controls_grid, text="Lower Threshold:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        threshold1_frame = ttk.Frame(controls_grid)
        threshold1_frame.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Scale(threshold1_frame, from_=0, to=255, variable=threshold1, orient=tk.HORIZONTAL, length=300).pack(side=tk.LEFT, padx=2)
        ttk.Label(threshold1_frame, textvariable=threshold1, width=3).pack(side=tk.LEFT, padx=5)
        
        # Threshold 2 (upper)
        ttk.Label(controls_grid, text="Upper Threshold:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        threshold2_frame = ttk.Frame(controls_grid)
        threshold2_frame.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Scale(threshold2_frame, from_=0, to=255, variable=threshold2, orient=tk.HORIZONTAL, length=300).pack(side=tk.LEFT, padx=2)
        ttk.Label(threshold2_frame, textvariable=threshold2, width=3).pack(side=tk.LEFT, padx=5)
        
        controls_grid.columnconfigure(1, weight=1)
        
        # Aperture size
        ttk.Label(controls_grid, text="Aperture Size:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        aperture_frame = ttk.Frame(controls_grid)
        aperture_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Only allow valid aperture sizes (3, 5, 7)
        for size in [3, 5, 7]:
            ttk.Radiobutton(aperture_frame, text=str(size), variable=aperture_size, value=size).pack(side=tk.LEFT, padx=10)
        
        # L2 Gradient
        ttk.Label(controls_grid, text="L2 Gradient:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        l2_frame = ttk.Frame(controls_grid)
        l2_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(l2_frame, text="Use L2 norm (more accurate but slower)", variable=l2gradient).pack(side=tk.LEFT, padx=2)
        
        # Update preview function
        def update_preview(*args):
            try:
                # Apply Canny edge detection
                edges = cv2.Canny(
                    image, 
                    threshold1.get(), 
                    threshold2.get(),
                    apertureSize=aperture_size.get(),
                    L2gradient=l2gradient.get()
                )
                
                # === SỬA PIL IMPORT ===
                # Display original image
                if len(image.shape) > 2 and image.shape[2] > 1:
                    display_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    display_img = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                
                display_img_resized = cv2.resize(display_img, (preview_w, preview_h))
                img1 = self.Image.fromarray(display_img_resized)
                img1_tk = self.ImageTk.PhotoImage(img1)
                # ======================
                
                original_canvas.delete("all")
                original_canvas.create_image(preview_w//2, preview_h//2, image=img1_tk)
                original_canvas.image = img1_tk
                
                # === SỬA PIL IMPORT ===
                # Display edges
                # Convert edges to RGB for display
                edges_display = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
                edges_resized = cv2.resize(edges_display, (preview_w, preview_h))
                img2 = self.Image.fromarray(edges_resized)
                img2_tk = self.ImageTk.PhotoImage(img2)
                # ======================
                
                edge_canvas.delete("all")
                edge_canvas.create_image(preview_w//2, preview_h//2, image=img2_tk)
                edge_canvas.image = img2_tk
                
            except Exception as e:
                # If error occurs, show message in canvas
                edge_canvas.delete("all")
                edge_canvas.create_text(preview_w//2, preview_h//2, text=str(e), fill="red")
        
        # Register callbacks
        threshold1.trace("w", update_preview)
        threshold2.trace("w", update_preview)
        aperture_size.trace("w", update_preview)
        l2gradient.trace("w", update_preview)
        
        # Update preview initially
        update_preview()
        
        # Action buttons
        def apply_edge_detection():
            nonlocal result
            try:
                # Apply Canny edge detection
                edges = cv2.Canny(
                    image, 
                    threshold1.get(), 
                    threshold2.get(),
                    apertureSize=aperture_size.get(),
                    L2gradient=l2gradient.get()
                )
                
                # Create code string
                code = f"edges = cv2.Canny(image, {threshold1.get()}, {threshold2.get()}, apertureSize={aperture_size.get()}, L2gradient={l2gradient.get()})\n"
                
                result = (edges, code)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply Canny edge detection: {str(e)}")
        
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_edge_detection).pack(side=tk.RIGHT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        return result
