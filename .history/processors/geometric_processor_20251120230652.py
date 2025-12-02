"""
Geometric Transformation Processor

Handles resize, flip, rotate, move, and perspective transformations.
This imports the original implementations from process_monolithic_backup.py
"""

import sys
import os
import cv2

# Add parent directory to Python path to import from backup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class GeometricProcessor:
    """Processor for geometric transformations - wraps original implementation."""
    
    def __init__(self, Image=None, ImageTk=None):
        """Initialize with PIL dependencies."""
        # Create instance of monolithic class with same PIL deps
        self._monolithic = MonolithicFP(Image, ImageTk)
    
    # Quick operations (no dialog)
    def rotate_image(self, image):
        """Rotate image by 90 degrees clockwise."""
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE), "cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)\n"
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
    def flip_Horizontal_image(self, image):
        """Flip image horizontally."""
        return cv2.flip(image, 1), "cv2.flip(image, 1)  # Horizontal flip\n"
    
    def flip_Vertical_image(self, image):
        """Flip image vertically."""
        return cv2.flip(image, 0), "cv2.flip(image, 0)  # Vertical flip\n"
    
    # Dialog operations - delegate to original
    def resize_image(self, image):
        """Resize image with custom dimensions - delegates to original."""
        return self._monolithic.resize_image(image)
    
    def flip_image(self, image):
        """Flip image with dialog - delegates to original."""
        return self._monolithic.flip_image(image)
    
    def rotationMatrix2d(self, image):
        """Apply custom rotation - delegates to original."""
        return self._monolithic.rotationMatrix2d(image)
    
    def move_image(self, image):
        """Translate/move image - delegates to original."""
        return self._monolithic.move_image(image)
    
    def perspectiveTransform(self, image):
        """Apply perspective transformation - delegates to original."""
        return self._monolithic.perspectiveTransform(image)

