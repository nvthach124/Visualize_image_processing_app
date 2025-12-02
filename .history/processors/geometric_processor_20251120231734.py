"""
Geometric Transformation Processor

Handles resize, flip, rotate, move, and perspective transformations.
This imports the original implementations from process_monolithic_backup.py
"""

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from .base_processor import BaseProcessor



# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class GeometricProcessor(BaseProcessor):
    """Processor for geometric transformations - wraps original implementation."""
    
    def __init__(self, Image=None, ImageTk=None):
        """Initialize with PIL dependencies."""
        # Create instance of monolithic class with same PIL deps
        self._monolithic = MonolithicFP(Image, ImageTk)
    
    # Quick operations (no dialog)
    def rotate_image(self, image):
        """Rotate image by 90 degrees clockwise."""
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE), "cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)\n"
    
    def flip_Horizontal_image(self, image):
        """Flip image horizontally."""
        return cv2.flip(image, 1), "cv2.flip(image, 1)  # Horizontal flip\n"
    
    def flip_Vertical_image(self, image):
        """Flip image vertically."""
        return cv2.flip(image, 0), "cv2.flip(image, 0)  # Vertical flip\n"
    
    # Dialog operations - delegate to original
    def resize_image(self, image):
        """Resize image with custom dimensions or percentage."""
        # Create dialog for custom resize
        result = None
        dialog = tk.Toplevel()
        dialog.title("Resize Image")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make dialog modal
        
        # Get original dimensions
        h, w = image.shape[:2]
        
        tk.Label(dialog, text="Original dimensions:", font=("Arial", 12)).pack(pady=(10, 5))
        tk.Label(dialog, text=f"Width: {w}px, Height: {h}px", font=("Arial", 11)).pack(pady=(0, 10))
        
        # Create frame for resize options
        options_frame = ttk.Frame(dialog)
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Variables
        resize_mode = tk.StringVar(value="dimensions")
        maintain_aspect = tk.BooleanVar(value=True)
        width_var = tk.IntVar(value=w)
        height_var = tk.IntVar(value=h)
        percent_var = tk.DoubleVar(value=100.0)
        
        # Functions to update fields
        def update_by_percent(*args):
            if resize_mode.get() == "percent":
                p = percent_var.get() / 100.0
                width_var.set(int(w * p))
                height_var.set(int(h * p))
        
        def update_height(*args):
            if maintain_aspect.get() and resize_mode.get() == "dimensions":
                ratio = w / h
                new_height = int(width_var.get() / ratio)
                height_var.set(new_height)
                percent_var.set(round(width_var.get() / w * 100, 1))
        
        def update_width(*args):
            if maintain_aspect.get() and resize_mode.get() == "dimensions":
                ratio = w / h
                new_width = int(height_var.get() * ratio)
                width_var.set(new_width)
                percent_var.set(round(height_var.get() / h * 100, 1))
        
        def mode_changed(*args):
            if resize_mode.get() == "percent":
                percent_frame.pack(fill=tk.X, pady=10)
                dimensions_frame.pack_forget()
                update_by_percent()
            else:
                dimensions_frame.pack(fill=tk.X, pady=10)
                percent_frame.pack_forget()
        
        # Create resize options
        modes_frame = ttk.Frame(options_frame)
        modes_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(modes_frame, text="Dimensions", variable=resize_mode, 
                      value="dimensions", command=mode_changed).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(modes_frame, text="Percentage", variable=resize_mode, 
                      value="percent", command=mode_changed).pack(side=tk.LEFT, padx=5)
        
        # Dimensions frame
        dimensions_frame = ttk.Frame(options_frame)
        dimensions_frame.pack(fill=tk.X, pady=10)
        
        width_frame = ttk.Frame(dimensions_frame)
        width_frame.pack(fill=tk.X, pady=5)
        ttk.Label(width_frame, text="Width:").pack(side=tk.LEFT, padx=5)
        width_entry = ttk.Entry(width_frame, textvariable=width_var, width=10)
        width_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(width_frame, text="px").pack(side=tk.LEFT)
        
        height_frame = ttk.Frame(dimensions_frame)
        height_frame.pack(fill=tk.X, pady=5)
        ttk.Label(height_frame, text="Height:").pack(side=tk.LEFT, padx=5)
        height_entry = ttk.Entry(height_frame, textvariable=height_var, width=10)
        height_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(height_frame, text="px").pack(side=tk.LEFT)
        
        # Percentage frame
        percent_frame = ttk.Frame(options_frame)
        
        percent_scale = ttk.Scale(percent_frame, from_=1, to=200, variable=percent_var, 
                                orient=tk.HORIZONTAL, length=200)
        percent_scale.pack(pady=5, fill=tk.X)
        
        percent_value_frame = ttk.Frame(percent_frame)
        percent_value_frame.pack(fill=tk.X, pady=5)
        ttk.Label(percent_value_frame, text="Scale:").pack(side=tk.LEFT, padx=5)
        percent_entry = ttk.Entry(percent_value_frame, textvariable=percent_var, width=10)
        percent_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(percent_value_frame, text="%").pack(side=tk.LEFT)
        
        # Aspect ratio checkbox
        ttk.Checkbutton(options_frame, text="Maintain aspect ratio", variable=maintain_aspect).pack(pady=10)
        
        # Register callbacks
        width_var.trace("w", update_height)
        height_var.trace("w", update_width)
        percent_var.trace("w", update_by_percent)
        
        # Control buttons
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def resize_ok():
            nonlocal result
            try:
                new_width = width_var.get()
                new_height = height_var.get()
                
                if new_width <= 0 or new_height <= 0:
                    messagebox.showerror("Error", "Width and height must be positive values")
                    return
                
                resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                result = (resized, f"cv2.resize(image, ({new_width}, {new_height}), interpolation=cv2.INTER_AREA)\n")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to resize image: {str(e)}")
        
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Resize", command=resize_ok).pack(side=tk.RIGHT, padx=5)
        
        # Initial setup - hide percent frame initially
        if resize_mode.get() == "dimensions":
            percent_frame.pack_forget()
        else:
            dimensions_frame.pack_forget()
        
        # Wait for dialog to close
        dialog.wait_window()
        return result

    def flip_image(self, image):
        """Flip image horizontally, vertically, or both."""
        # Create dialog for flip options
        result = None
        dialog = tk.Toplevel()
        dialog.title("Flip Image")
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Variables
        flip_mode = tk.IntVar(value=1)  # Default horizontal flip
        
        # Options frame
        options_frame = ttk.Frame(dialog)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(options_frame, text="Flip Direction:", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(options_frame, text="Horizontal (left/right)", variable=flip_mode, value=1).pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(options_frame, text="Vertical (up/down)", variable=flip_mode, value=0).pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(options_frame, text="Both horizontal and vertical", variable=flip_mode, value=-1).pack(anchor=tk.W, pady=5)
        
        # Control buttons
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def flip_ok():
            nonlocal result
            try:
                mode = flip_mode.get()
                flipped = cv2.flip(image, mode)
                result = (flipped, f"cv2.flip(image, {mode})  # {['Vertical', 'Horizontal', 'Both'][mode+1]} flip\n")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to flip image: {str(e)}")
        
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=flip_ok).pack(side=tk.RIGHT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        return result

    def move_image(self, image):
        """Translate/move image in X and Y directions."""
        result = None
        dialog = tk.Toplevel()
        dialog.title("Move Image")
        dialog.geometry("700x550")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Variables and setup
        h, w = image.shape[:2]
        tx = tk.IntVar(value=50)
        ty = tk.IntVar(value=50)
        
        # Create frames
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Move Image", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview area
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original and result previews
        orig_frame = ttk.LabelFrame(preview_frame, text="Original")
        orig_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        result_frame = ttk.LabelFrame(preview_frame, text="Result")
        result_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Canvases for image display
        scale = min(300/w, 200/h)
        preview_w, preview_h = int(w*scale), int(h*scale)
        
        orig_canvas = tk.Canvas(orig_frame, width=preview_w, height=preview_h, bg="lightgray")
        orig_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        result_canvas = tk.Canvas(result_frame, width=preview_w, height=preview_h, bg="lightgray")
        result_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # X translation
        ttk.Label(controls_frame, text="X Translation:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        x_scale = ttk.Scale(controls_frame, from_=-w//2, to=w//2, variable=tx, orient=tk.HORIZONTAL, length=300)
        x_scale.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(controls_frame, textvariable=tx, width=4).grid(row=0, column=2, padx=5)
        
        # Y translation
        ttk.Label(controls_frame, text="Y Translation:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        y_scale = ttk.Scale(controls_frame, from_=-h//2, to=h//2, variable=ty, orient=tk.HORIZONTAL, length=300)
        y_scale.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(controls_frame, textvariable=ty, width=4).grid(row=1, column=2, padx=5)
        
        controls_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Apply", command=lambda: apply_move()).pack(side=tk.RIGHT, padx=5)
        
        def update_preview(*args):
            try:
                # Calculate translation matrix and apply it
                M = np.array([[1, 0, tx.get()], [0, 1, ty.get()]], dtype=np.float32)
                moved = cv2.warpAffine(image, M, (w, h))
                
                # === SỬA PIL IMPORT ===
                # Show original image
                if len(image.shape) > 2:
                    orig_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    orig_img = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                
                orig_resized = cv2.resize(orig_img, (preview_w, preview_h))
                orig_tk = self.ImageTk.PhotoImage(self.Image.fromarray(orig_resized))
                # ======================
                
                orig_canvas.delete("all")
                orig_canvas.create_image(preview_w//2, preview_h//2, image=orig_tk)
                orig_canvas.image = orig_tk  # Keep reference
                
                # === SỬA PIL IMPORT ===
                # Show result image
                if len(moved.shape) > 2:
                    result_img = cv2.cvtColor(moved, cv2.COLOR_BGR2RGB)
                else:
                    result_img = cv2.cvtColor(moved, cv2.COLOR_GRAY2RGB)
                
                result_resized = cv2.resize(result_img, (preview_w, preview_h))
                result_tk = self.ImageTk.PhotoImage(self.Image.fromarray(result_resized))
                # ======================
                
                result_canvas.delete("all")
                result_canvas.create_image(preview_w//2, preview_h//2, image=result_tk)
                result_canvas.image = result_tk  # Keep reference
            except Exception as e:
                print(f"Preview error: {str(e)}")
        
        def apply_move():
            nonlocal result
            try:
                # Apply the transformation
                M = np.array([[1, 0, tx.get()], [0, 1, ty.get()]], dtype=np.float32)
                moved_img = cv2.warpAffine(image, M, (w, h))
                
                # Generate code representation
                code = f"M = np.array([[1, 0, {tx.get()}], [0, 1, {ty.get()}]], dtype=np.float32)\n"
                code += f"moved_img = cv2.warpAffine(image, M, ({w}, {h}))\n"
                
                result = (moved_img, code)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move image: {str(e)}")
        
        # Register callbacks and show initial preview
        tx.trace("w", update_preview)
        ty.trace("w", update_preview)
        update_preview()
        
        # Wait for the dialog to close
        dialog.wait_window()
        return result

    def rotationMatrix2d(self, image):
        """Apply custom rotation with angle and scale using rotation matrix."""
        result = None
        dialog = tk.Toplevel()
        dialog.title("Rotate Image")
        dialog.geometry("700x550")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Variables and setup
        h, w = image.shape[:2]
        angle = tk.DoubleVar(value=45)
        scale = tk.DoubleVar(value=1.0)
        center_x = tk.IntVar(value=w//2)
        center_y = tk.IntVar(value=h//2)
        use_center = tk.BooleanVar(value=True)
        
        # Create frames
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Rotate Image", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview area
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original and result previews
        orig_frame = ttk.LabelFrame(preview_frame, text="Original")
        orig_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        result_frame = ttk.LabelFrame(preview_frame, text="Result")
        result_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Canvases for image display
        scale_factor = min(300/w, 200/h)
        preview_w, preview_h = int(w*scale_factor), int(h*scale_factor)
        
        orig_canvas = tk.Canvas(orig_frame, width=preview_w, height=preview_h, bg="lightgray")
        orig_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        result_canvas = tk.Canvas(result_frame, width=preview_w, height=preview_h, bg="lightgray")
        result_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Angle control
        ttk.Label(controls_frame, text="Angle (degrees):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        angle_scale = ttk.Scale(controls_frame, from_=-180, to=180, variable=angle, orient=tk.HORIZONTAL, length=300)
        angle_scale.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(controls_frame, textvariable=angle, width=4).grid(row=0, column=2, padx=5)
        
        # Scale control
        ttk.Label(controls_frame, text="Scale:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        scale_scale = ttk.Scale(controls_frame, from_=0.1, to=3.0, variable=scale, orient=tk.HORIZONTAL, length=300)
        scale_scale.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(controls_frame, textvariable=scale, width=4).grid(row=1, column=2, padx=5)
        
        controls_frame.columnconfigure(1, weight=1)
        
        # Center controls
        center_frame = ttk.Frame(controls_frame)
        center_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Checkbutton(center_frame, text="Use image center", variable=use_center).pack(anchor=tk.W, pady=5)
        
        center_coords = ttk.Frame(center_frame)
        center_coords.pack(fill=tk.X, pady=5)
        
        ttk.Label(center_coords, text="Center X:").pack(side=tk.LEFT, padx=5)
        center_x_entry = ttk.Entry(center_coords, textvariable=center_x, width=5)
        center_x_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(center_coords, text="Center Y:").pack(side=tk.LEFT, padx=5)
        center_y_entry = ttk.Entry(center_coords, textvariable=center_y, width=5)
        center_y_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Apply", command=lambda: apply_rotation()).pack(side=tk.RIGHT, padx=5)
        
        def update_center_state(*args):
            if use_center.get():
                center_x.set(w // 2)
                center_y.set(h // 2)
                center_x_entry.config(state="disabled")
                center_y_entry.config(state="disabled")
            else:
                center_x_entry.config(state="normal")
                center_y_entry.config(state="normal")
        
        def update_preview(*args):
            try:
                # Apply rotation
                center = (center_x.get(), center_y.get())
                M = cv2.getRotationMatrix2D(center, angle.get(), scale.get())
                rotated = cv2.warpAffine(image, M, (w, h))
                
                # === SỬA PIL IMPORT ===
                # Show original image with center point
                if len(image.shape) > 2:
                    orig_img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
                else:
                    orig_img = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)
                
                # Draw center point on original
                cv2.circle(orig_img, center, 5, (255, 0, 0), -1)
                
                orig_resized = cv2.resize(orig_img, (preview_w, preview_h))
                orig_tk = self.ImageTk.PhotoImage(self.Image.fromarray(orig_resized))
                # ======================
                
                orig_canvas.delete("all")
                orig_canvas.create_image(preview_w//2, preview_h//2, image=orig_tk)
                orig_canvas.image = orig_tk  # Keep reference
                
                # === SỬA PIL IMPORT ===
                # Show result image
                if len(rotated.shape) > 2:
                    result_img = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
                else:
                    result_img = cv2.cvtColor(rotated, cv2.COLOR_GRAY2RGB)
                
                result_resized = cv2.resize(result_img, (preview_w, preview_h))
                result_tk = self.ImageTk.PhotoImage(self.Image.fromarray(result_resized))
                # ======================
                
                result_canvas.delete("all")
                result_canvas.create_image(preview_w//2, preview_h//2, image=result_tk)
                result_canvas.image = result_tk  # Keep reference
            except Exception as e:
                print(f"Preview error: {str(e)}")
        
        def apply_rotation():
            nonlocal result
            try:
                # Apply the transformation
                center = (center_x.get(), center_y.get())
                M = cv2.getRotationMatrix2D(center, angle.get(), scale.get())
                rotated_img = cv2.warpAffine(image, M, (w, h))
                
                # Generate code representation
                code = f"# Rotate image around ({center[0]}, {center[1]}) by {angle.get()} degrees with scale {scale.get()}\n"
                code += f"M = cv2.getRotationMatrix2D(({center[0]}, {center[1]}), {angle.get()}, {scale.get()})\n"
                code += f"rotated_img = cv2.warpAffine(image, M, ({w}, {h}))\n"
                
                result = (rotated_img, code)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rotate image: {str(e)}")
        
        # Register callbacks and show initial preview
        use_center.trace("w", update_center_state)
        angle.trace("w", update_preview)
        scale.trace("w", update_preview)
        center_x.trace("w", update_preview)
        center_y.trace("w", update_preview)
        
        update_center_state()  # Initial state
        update_preview()
        
        # Wait for the dialog to close
        dialog.wait_window()
        return result

    def perspectiveTransform(self, image):
        """Apply perspective transformation with interactive point selection."""
        result = None
        dialog = tk.Toplevel()
        dialog.title("Perspective Transform")
        dialog.geometry("800x800")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Variables and setup
        h, w = image.shape[:2]
        
        # Default source points (approximately 25% in from corners)
        src_points = [
            [int(w * 0.25), int(h * 0.25)],  # Top-left
            [int(w * 0.75), int(h * 0.25)],  # Top-right
            [int(w * 0.25), int(h * 0.75)],  # Bottom-left
            [int(w * 0.75), int(h * 0.75)]   # Bottom-right
        ]
        
        # Default destination points (rectangle)
        dst_points = [
            [0, 0],            # Top-left
            [w - 1, 0],        # Top-right
            [0, h - 1],        # Bottom-left
            [w - 1, h - 1]     # Bottom-right
        ]
        
        # Create variables for points
        src_x_vars = [tk.IntVar(value=p[0]) for p in src_points]
        src_y_vars = [tk.IntVar(value=p[1]) for p in src_points]
        dst_x_vars = [tk.IntVar(value=p[0]) for p in dst_points]
        dst_y_vars = [tk.IntVar(value=p[1]) for p in dst_points]
        
        # Point labels for UI
        point_labels = ["Top-left", "Top-right", "Bottom-left", "Bottom-right"]
        selected_point = tk.IntVar(value=-1)  # For interactive selection
        
        # Create main layout
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Perspective Transform", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview area
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Source and destination preview frames
        src_frame = ttk.LabelFrame(preview_frame, text="Source Image")
        src_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        dst_frame = ttk.LabelFrame(preview_frame, text="Result")
        dst_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Canvas for previews
        scale_factor = min(350/w, 250/h)
        preview_w, preview_h = int(w*scale_factor), int(h*scale_factor)
        
        src_canvas = tk.Canvas(src_frame, width=preview_w, height=preview_h, bg="lightgray")
        src_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        dst_canvas = tk.Canvas(dst_frame, width=preview_w, height=preview_h, bg="lightgray")
        dst_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls with tabs
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Notebook for tabbed interface
        tabs = ttk.Notebook(controls_frame)
        tabs.pack(fill=tk.BOTH, expand=True)
        
        # Tab for source points
        src_tab = ttk.Frame(tabs)
        tabs.add(src_tab, text="Source Points")
        
        # Tab for destination points
        dst_tab = ttk.Frame(tabs)
        tabs.add(dst_tab, text="Destination Points")
        
        # Source points controls
        src_controls = ttk.Frame(src_tab, padding=10)
        src_controls.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(src_controls, text="Click on image to set selected point").pack(anchor=tk.W, pady=5)
        
        # Point selection
        point_select_frame = ttk.Frame(src_controls)
        point_select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(point_select_frame, text="Select point:").pack(side=tk.LEFT, padx=5)
        for i, label in enumerate(point_labels):
            ttk.Radiobutton(
                point_select_frame, 
                text=label, 
                variable=selected_point, 
                value=i
            ).pack(side=tk.LEFT, padx=10)
        
        # Source points coordinates
        src_coords_frame = ttk.Frame(src_controls)
        src_coords_frame.pack(fill=tk.X, pady=10)
        
        # Table header
        ttk.Label(src_coords_frame, text="Point", width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(src_coords_frame, text="X", width=10).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(src_coords_frame, text="Y", width=10).grid(row=0, column=2, padx=5, pady=5)
        
        # Table rows
        for i, label in enumerate(point_labels):
            ttk.Label(src_coords_frame, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky=tk.W)
            ttk.Entry(src_coords_frame, textvariable=src_x_vars[i], width=8).grid(row=i+1, column=1, padx=5, pady=5)
            ttk.Entry(src_coords_frame, textvariable=src_y_vars[i], width=8).grid(row=i+1, column=2, padx=5, pady=5)
        
        # Destination points controls
        dst_controls = ttk.Frame(dst_tab, padding=10)
        dst_controls.pack(fill=tk.BOTH, expand=True)
        
        # Presets
        preset_frame = ttk.Frame(dst_controls)
        preset_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(preset_frame, text="Presets:").pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Rectangle", command=lambda: set_rect_preset()).pack(side=tk.LEFT, padx=5)
        
        # Destination coordinates
        dst_coords_frame = ttk.Frame(dst_controls)
        dst_coords_frame.pack(fill=tk.X, pady=10)
        
        # Table header
        ttk.Label(dst_coords_frame, text="Point", width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(dst_coords_frame, text="X", width=10).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(dst_coords_frame, text="Y", width=10).grid(row=0, column=2, padx=5, pady=5)
        
        # Table rows
        for i, label in enumerate(point_labels):
            ttk.Label(dst_coords_frame, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky=tk.W)
            ttk.Entry(dst_coords_frame, textvariable=dst_x_vars[i], width=8).grid(row=i+1, column=1, padx=5, pady=5)
            ttk.Entry(dst_coords_frame, textvariable=dst_y_vars[i], width=8).grid(row=i+1, column=2, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Apply", command=lambda: apply_transform()).pack(side=tk.RIGHT, padx=5)
        
        # Functions
        def set_rect_preset():
            # Set destination to rectangle
            dst_x_vars[0].set(0)
            dst_y_vars[0].set(0)
            dst_x_vars[1].set(w - 1)
            dst_y_vars[1].set(0)
            dst_x_vars[2].set(0)
            dst_y_vars[2].set(h - 1)
            dst_x_vars[3].set(w - 1)
            dst_y_vars[3].set(h - 1)
            update_preview()
        
        def canvas_click(event):
            # Get selected point
            idx = selected_point.get()
            if idx < 0 or idx > 3:
                return
                
            # Convert canvas coordinates to image coordinates
            img_x = int(event.x / scale_factor)
            img_y = int(event.y / scale_factor)
            
            # Ensure coordinates are within image bounds
            img_x = max(0, min(img_x, w-1))
            img_y = max(0, min(img_y, h-1))
            
            # Update source point
            src_x_vars[idx].set(img_x)
            src_y_vars[idx].set(img_y)
            update_preview()
        
        def update_preview(*args):
            try:
                # Get points
                src_pts = np.array([
                    [src_x_vars[i].get(), src_y_vars[i].get()] for i in range(4)
                ], dtype=np.float32)
                
                dst_pts = np.array([
                    [dst_x_vars[i].get(), dst_y_vars[i].get()] for i in range(4)
                ], dtype=np.float32)
                
                # Apply perspective transform
                M = cv2.getPerspectiveTransform(src_pts, dst_pts)
                warped = cv2.warpPerspective(image, M, (w, h))
                
                # === SỬA PIL IMPORT ===
                # Display source image with points
                if len(image.shape) > 2:
                    src_img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
                else:
                    src_img = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)
                
                # Draw points and lines on source image
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
                for i in range(4):
                    pt = (src_x_vars[i].get(), src_y_vars[i].get())
                    cv2.circle(src_img, pt, 5, colors[i], -1)
                    cv2.putText(src_img, str(i+1), (pt[0]+5, pt[1]+5), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[i], 2)
                
                # Draw lines connecting the points
                cv2.line(src_img, (src_x_vars[0].get(), src_y_vars[0].get()), 
                        (src_x_vars[1].get(), src_y_vars[1].get()), (255, 255, 255), 1)
                cv2.line(src_img, (src_x_vars[1].get(), src_y_vars[1].get()), 
                        (src_x_vars[3].get(), src_y_vars[3].get()), (255, 255, 255), 1)
                cv2.line(src_img, (src_x_vars[3].get(), src_y_vars[3].get()), 
                        (src_x_vars[2].get(), src_y_vars[2].get()), (255, 255, 255), 1)
                cv2.line(src_img, (src_x_vars[2].get(), src_y_vars[2].get()), 
                        (src_x_vars[0].get(), src_y_vars[0].get()), (255, 255, 255), 1)
                
                src_resized = cv2.resize(src_img, (preview_w, preview_h))
                src_tk = self.ImageTk.PhotoImage(self.Image.fromarray(src_resized))
                # ======================
                
                src_canvas.delete("all")
                src_canvas.create_image(preview_w//2, preview_h//2, image=src_tk)
                src_canvas.image = src_tk
                
                # === SỬA PIL IMPORT ===
                # Display destination/result image
                if len(warped.shape) > 2:
                    dst_img = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
                else:
                    dst_img = cv2.cvtColor(warped, cv2.COLOR_GRAY2RGB)
                
                dst_resized = cv2.resize(dst_img, (preview_w, preview_h))
                dst_tk = self.ImageTk.PhotoImage(self.Image.fromarray(dst_resized))
                # ======================
                
                dst_canvas.delete("all")
                dst_canvas.create_image(preview_w//2, preview_h//2, image=dst_tk)
                dst_canvas.image = dst_tk
                
            except Exception as e:
                print(f"Preview error: {str(e)}")
        
        def apply_transform():
            nonlocal result
            try:
                # Get points
                src_pts = np.array([
                    [src_x_vars[i].get(), src_y_vars[i].get()] for i in range(4)
                ], dtype=np.float32)
                
                dst_pts = np.array([
                    [dst_x_vars[i].get(), dst_y_vars[i].get()] for i in range(4)
                ], dtype=np.float32)
                
                # Apply perspective transform
                M = cv2.getPerspectiveTransform(src_pts, dst_pts)
                warped = cv2.warpPerspective(image, M, (w, h))
                
                # Generate code
                code = "# Perspective transform\n"
                code += f"src_points = np.float32({src_pts.tolist()})\n"
                code += f"dst_points = np.float32({dst_pts.tolist()})\n"
                code += "M = cv2.getPerspectiveTransform(src_points, dst_points)\n"
                code += f"warped = cv2.warpPerspective(image, M, ({w}, {h}))\n"
                
                result = (warped, code)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply perspective transform: {str(e)}")
        
        # Bind events
        src_canvas.bind("<Button-1>", canvas_click)
        
        # Register callbacks
        for var in src_x_vars + src_y_vars + dst_x_vars + dst_y_vars:
            var.trace("w", update_preview)
        
        # Initial preview
        update_preview()
        
        dialog.wait_window()
        return result

