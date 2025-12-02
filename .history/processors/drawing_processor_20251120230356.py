"""
Drawing Utilities Processor

Handles drawing lines, rectangles, circles, and text on images.
This imports the original implementations from process_monolithic_backup.py
"""

import sys
import os
import cv2
import tkinter as tk
from tkinter import ttk

# Add parent directory to Python path to import from backup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the monolithic FunctionsProcessing class
from process_monolithic_backup import FunctionsProcessing as MonolithicFP


class DrawingProcessor:
    """Processor for drawing operations - wraps original implementation."""
    
   # ========================================================================
    # DRAWING UTILITIES
    # ========================================================================
    
    def draw_Line(self, image):
        """Draw lines on image with custom color and thickness."""
        # Create a copy of the image to preview
        img_copy = image.copy()
        
        result = None
        dialog = tk.Toplevel()
        dialog.title("Draw Line")
        dialog.geometry("600x600")
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
        pt1_x = tk.IntVar(value=50)
        pt1_y = tk.IntVar(value=50)
        pt2_x = tk.IntVar(value=450)
        pt2_y = tk.IntVar(value=50)
        thickness = tk.IntVar(value=2)
        color = tk.StringVar(value="#FF0000")  # Red
        
        # Title
        ttk.Label(top_frame, text="Draw Line", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview canvas
        h, w = image.shape[:2]
        scale = min(500/w, 300/h)
        preview_w, preview_h = int(w*scale), int(h*scale)
        
        canvas = tk.Canvas(preview_frame, width=preview_w, height=preview_h, bg="lightgray", bd=1, relief=tk.SOLID)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls
        controls_grid = ttk.Frame(controls_frame)
        controls_grid.pack(fill=tk.X, padx=5, pady=5)
        
        # Start point
        ttk.Label(controls_grid, text="Start Point:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        start_frame = ttk.Frame(controls_grid)
        start_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(start_frame, text="X:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(start_frame, textvariable=pt1_x, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(start_frame, text="Y:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(start_frame, textvariable=pt1_y, width=5).pack(side=tk.LEFT, padx=2)
        
        # End point
        ttk.Label(controls_grid, text="End Point:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        end_frame = ttk.Frame(controls_grid)
        end_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(end_frame, text="X:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(end_frame, textvariable=pt2_x, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(end_frame, text="Y:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(end_frame, textvariable=pt2_y, width=5).pack(side=tk.LEFT, padx=2)
        
        # Thickness
        ttk.Label(controls_grid, text="Thickness:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        thickness_frame = ttk.Frame(controls_grid)
        thickness_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Scale(thickness_frame, from_=1, to=20, variable=thickness, orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=2)
        ttk.Label(thickness_frame, textvariable=thickness).pack(side=tk.LEFT, padx=2)
        
        # Color
        ttk.Label(controls_grid, text="Color:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        color_frame = ttk.Frame(controls_grid)
        color_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        color_preview = tk.Canvas(color_frame, width=20, height=20, bg=color.get())
        color_preview.pack(side=tk.LEFT, padx=2)
        
        def choose_color():
            rgb_color = colorchooser.askcolor(color.get())
            if rgb_color[1]:
                color.set(rgb_color[1])
                color_preview.config(bg=rgb_color[1])
                update_preview()
        
        ttk.Button(color_frame, text="Select Color", command=choose_color).pack(side=tk.LEFT, padx=2)
        
        # Update preview function
        def update_preview(*args):
            # Convert hex color to BGR
            hex_color = color.get().lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            bgr_color = (b, g, r)
            
            # Draw line on copy
            img_copy = image.copy()
            cv2.line(img_copy, 
                    (pt1_x.get(), pt1_y.get()), 
                    (pt2_x.get(), pt2_y.get()), 
                    bgr_color, 
                    thickness.get())
            
            # Scale and display
            preview_img = cv2.resize(img_copy, (preview_w, preview_h))
            
            # Convert to RGB for Tkinter
            if len(preview_img.shape) == 2:  # Grayscale
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_GRAY2RGB)
            else:  # BGR
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB)
            
            try:
                # === SỬA PIL IMPORT ===
                img = self.Image.fromarray(preview_rgb)
                img_tk = self.ImageTk.PhotoImage(img)
                # ======================
                
                canvas.delete("all")
                canvas.create_image(preview_w//2, preview_h//2, image=img_tk)
                canvas.image = img_tk
            except Exception as e:
                # If PIL not available, just show a message
                canvas.delete("all")
                canvas.create_text(preview_w//2, preview_h//2, text=f"Preview error: {e}")
        
        # Register trace callbacks
        pt1_x.trace("w", update_preview)
        pt1_y.trace("w", update_preview)
        pt2_x.trace("w", update_preview)
        pt2_y.trace("w", update_preview)
        thickness.trace("w", update_preview)
        color.trace("w", update_preview)
        
        # Update preview initially
        update_preview()
        
        # Action buttons
        def apply_line():
            nonlocal result
            try:
                # Convert hex color to BGR
                hex_color = color.get().lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                bgr_color = (b, g, r)
                
                new_img = image.copy()
                cv2.line(new_img, 
                        (pt1_x.get(), pt1_y.get()), 
                        (pt2_x.get(), pt2_y.get()), 
                        bgr_color, 
                        thickness.get())
                
                result = (new_img, f"cv2.line(image, pt1=({pt1_x.get()}, {pt1_y.get()}), pt2=({pt2_x.get()}, {pt2_y.get()}), color={bgr_color}, thickness={thickness.get()})\n")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to draw line: {str(e)}")
        
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_line).pack(side=tk.RIGHT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        return result

    def draw_Rectangle(self, image):
        """Draw rectangles on image with custom color, thickness, and fill."""
        # Create a copy of the image to preview
        img_copy = image.copy()
        
        result = None
        dialog = tk.Toplevel()
        dialog.title("Draw Rectangle")
        dialog.geometry("600x600")
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
        pt1_x = tk.IntVar(value=80)
        pt1_y = tk.IntVar(value=80)
        pt2_x = tk.IntVar(value=300)
        pt2_y = tk.IntVar(value=300)
        thickness = tk.IntVar(value=2)
        color = tk.StringVar(value="#0000FF")  # Blue
        filled = tk.BooleanVar(value=False)
        
        # Title
        ttk.Label(top_frame, text="Draw Rectangle", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview canvas
        h, w = image.shape[:2]
        scale = min(500/w, 300/h)
        preview_w, preview_h = int(w*scale), int(h*scale)
        
        canvas = tk.Canvas(preview_frame, width=preview_w, height=preview_h, bg="lightgray", bd=1, relief=tk.SOLID)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls
        controls_grid = ttk.Frame(controls_frame)
        controls_grid.pack(fill=tk.X, padx=5, pady=5)
        
        # Top-left corner
        ttk.Label(controls_grid, text="Top-Left Corner:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        start_frame = ttk.Frame(controls_grid)
        start_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(start_frame, text="X:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(start_frame, textvariable=pt1_x, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(start_frame, text="Y:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(start_frame, textvariable=pt1_y, width=5).pack(side=tk.LEFT, padx=2)
        
        # Bottom-right corner
        ttk.Label(controls_grid, text="Bottom-Right Corner:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        end_frame = ttk.Frame(controls_grid)
        end_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(end_frame, text="X:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(end_frame, textvariable=pt2_x, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(end_frame, text="Y:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(end_frame, textvariable=pt2_y, width=5).pack(side=tk.LEFT, padx=2)
        
        # Thickness
        ttk.Label(controls_grid, text="Thickness:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        thickness_frame = ttk.Frame(controls_grid)
        thickness_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Scale(thickness_frame, from_=1, to=20, variable=thickness, orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=2)
        ttk.Label(thickness_frame, textvariable=thickness).pack(side=tk.LEFT, padx=2)
        ttk.Checkbutton(thickness_frame, text="Filled", variable=filled).pack(side=tk.LEFT, padx=10)
        
        # Color
        color_frame = ttk.Frame(controls_grid)
        color_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT, padx=5)
        
        color_preview = tk.Canvas(color_frame, width=20, height=20, bg=color.get())
        color_preview.pack(side=tk.LEFT, padx=2)
        
        def choose_color():
            rgb_color = colorchooser.askcolor(color.get())
            if rgb_color[1]:
                color.set(rgb_color[1])
                color_preview.config(bg=rgb_color[1])
                update_preview()
        
        ttk.Button(color_frame, text="Select Color", command=choose_color).pack(side=tk.LEFT, padx=2)
        
        # Update preview function
        def update_preview(*args):
            # Convert hex color to BGR
            hex_color = color.get().lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            bgr_color = (b, g, r)
            
            # Draw rectangle on copy
            img_copy = image.copy()
            
            # If filled, set thickness to -1
            thick = -1 if filled.get() else thickness.get()
            
            cv2.rectangle(img_copy, 
                        (pt1_x.get(), pt1_y.get()), 
                        (pt2_x.get(), pt2_y.get()), 
                        bgr_color, 
                        thick)
            
            # Scale and display
            preview_img = cv2.resize(img_copy, (preview_w, preview_h))
            
            # Convert to RGB for Tkinter
            if len(preview_img.shape) == 2:  # Grayscale
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_GRAY2RGB)
            else:  # BGR
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB)
            
            try:
                # === SỬA PIL IMPORT ===
                img = self.Image.fromarray(preview_rgb)
                img_tk = self.ImageTk.PhotoImage(img)
                # ======================
                
                canvas.delete("all")
                canvas.create_image(preview_w//2, preview_h//2, image=img_tk)
                canvas.image = img_tk
            except Exception as e:
                # If PIL not available, just show a message
                canvas.delete("all")
                canvas.create_text(preview_w//2, preview_h//2, text=f"Preview error: {e}")
        
        # Register trace callbacks
        pt1_x.trace("w", update_preview)
        pt1_y.trace("w", update_preview)
        pt2_x.trace("w", update_preview)
        pt2_y.trace("w", update_preview)
        thickness.trace("w", update_preview)
        color.trace("w", update_preview)
        filled.trace("w", update_preview)
        
        # Update preview initially
        update_preview()
        
        # Action buttons
        def apply_rectangle():
            nonlocal result
            try:
                # Convert hex color to BGR
                hex_color = color.get().lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                bgr_color = (b, g, r)
                
                new_img = image.copy()
                
                # If filled, set thickness to -1
                thick = -1 if filled.get() else thickness.get()
                
                cv2.rectangle(new_img, 
                            (pt1_x.get(), pt1_y.get()), 
                            (pt2_x.get(), pt2_y.get()), 
                            bgr_color, 
                            thick)
                
                fill_text = "filled " if filled.get() else ""
                result = (new_img, f"cv2.rectangle(image, pt1=({pt1_x.get()}, {pt1_y.get()}), pt2=({pt2_x.get()}, {pt2_y.get()}), color={bgr_color}, thickness={thick})  # {fill_text}rectangle\n")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to draw rectangle: {str(e)}")
        
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_rectangle).pack(side=tk.RIGHT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        return result

    def draw_Circle(self, image):
        """Draw circles on image with custom color, thickness, and fill."""
        # Create a copy of the image to preview
        img_copy = image.copy()
        
        result = None
        dialog = tk.Toplevel()
        dialog.title("Draw Circle")
        dialog.geometry("600x600")
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
        center_x = tk.IntVar(value=400)
        center_y = tk.IntVar(value=300)
        radius = tk.IntVar(value=50)
        thickness = tk.IntVar(value=2)
        color = tk.StringVar(value="#FF0000")  # Red
        filled = tk.BooleanVar(value=False)
        
        # Title
        ttk.Label(top_frame, text="Draw Circle", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview canvas
        h, w = image.shape[:2]
        scale = min(500/w, 300/h)
        preview_w, preview_h = int(w*scale), int(h*scale)
        
        canvas = tk.Canvas(preview_frame, width=preview_w, height=preview_h, bg="lightgray", bd=1, relief=tk.SOLID)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls
        controls_grid = ttk.Frame(controls_frame)
        controls_grid.pack(fill=tk.X, padx=5, pady=5)
        
        # Center point
        ttk.Label(controls_grid, text="Center Point:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        center_frame = ttk.Frame(controls_grid)
        center_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(center_frame, text="X:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(center_frame, textvariable=center_x, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(center_frame, text="Y:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(center_frame, textvariable=center_y, width=5).pack(side=tk.LEFT, padx=2)
        
        # Radius
        ttk.Label(controls_grid, text="Radius:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        radius_frame = ttk.Frame(controls_grid)
        radius_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Scale(radius_frame, from_=1, to=200, variable=radius, orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=2)
        ttk.Label(radius_frame, textvariable=radius).pack(side=tk.LEFT, padx=2)
        
        # Thickness
        thickness_frame = ttk.Frame(controls_grid)
        thickness_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(thickness_frame, text="Thickness:").pack(side=tk.LEFT, padx=5)
        ttk.Scale(thickness_frame, from_=1, to=20, variable=thickness, orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=2)
        ttk.Label(thickness_frame, textvariable=thickness).pack(side=tk.LEFT, padx=2)
        ttk.Checkbutton(thickness_frame, text="Filled", variable=filled).pack(side=tk.LEFT, padx=10)
        
        # Color
        color_frame = ttk.Frame(controls_grid)
        color_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT, padx=5)
        
        color_preview = tk.Canvas(color_frame, width=20, height=20, bg=color.get())
        color_preview.pack(side=tk.LEFT, padx=2)
        
        def choose_color():
            rgb_color = colorchooser.askcolor(color.get())
            if rgb_color[1]:
                color.set(rgb_color[1])
                color_preview.config(bg=rgb_color[1])
                update_preview()
        
        ttk.Button(color_frame, text="Select Color", command=choose_color).pack(side=tk.LEFT, padx=2)
        
        # Update preview function
        def update_preview(*args):
            # Convert hex color to BGR
            hex_color = color.get().lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            bgr_color = (b, g, r)
            
            # Draw circle on copy
            img_copy = image.copy()
            
            # If filled, set thickness to -1
            thick = -1 if filled.get() else thickness.get()
            
            cv2.circle(img_copy, 
                      (center_x.get(), center_y.get()), 
                      radius.get(), 
                      bgr_color, 
                      thick)
            
            # Scale and display
            preview_img = cv2.resize(img_copy, (preview_w, preview_h))
            
            # Convert to RGB for Tkinter
            if len(preview_img.shape) == 2:  # Grayscale
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_GRAY2RGB)
            else:  # BGR
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB)
            
            try:
                # === SỬA PIL IMPORT ===
                img = self.Image.fromarray(preview_rgb)
                img_tk = self.ImageTk.PhotoImage(img)
                # ======================
                
                canvas.delete("all")
                canvas.create_image(preview_w//2, preview_h//2, image=img_tk)
                canvas.image = img_tk
            except Exception as e:
                # If PIL not available, just show a message
                canvas.delete("all")
                canvas.create_text(preview_w//2, preview_h//2, text=f"Preview error: {e}")
        
        # Register trace callbacks
        center_x.trace("w", update_preview)
        center_y.trace("w", update_preview)
        radius.trace("w", update_preview)
        thickness.trace("w", update_preview)
        color.trace("w", update_preview)
        filled.trace("w", update_preview)
        
        # Update preview initially
        update_preview()
        
        # Action buttons
        def apply_circle():
            nonlocal result
            try:
                # Convert hex color to BGR
                hex_color = color.get().lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                bgr_color = (b, g, r)
                
                new_img = image.copy()
                
                # If filled, set thickness to -1
                thick = -1 if filled.get() else thickness.get()
                
                cv2.circle(new_img, 
                          (center_x.get(), center_y.get()), 
                          radius.get(), 
                          bgr_color, 
                          thick)
                
                fill_text = "filled " if filled.get() else ""
                result = (new_img, f"cv2.circle(image, center=({center_x.get()}, {center_y.get()}), radius={radius.get()}, color={bgr_color}, thickness={thick})  # {fill_text}circle\n")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to draw circle: {str(e)}")
        
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_circle).pack(side=tk.RIGHT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        return result

    def draw_text(self, image):
        """Add text to image with custom font, size, color, and position."""
        # Create a copy of the image to preview
        img_copy = image.copy()
        
        result = None
        dialog = tk.Toplevel()
        dialog.title("Add Text")
        dialog.geometry("800x800")
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
        text = tk.StringVar(value="Hello World")
        pos_x = tk.IntVar(value=200)
        pos_y = tk.IntVar(value=200)
        font_scale = tk.DoubleVar(value=1.0)
        thickness = tk.IntVar(value=2)
        color = tk.StringVar(value="#FF0000")  # Red
        font_face = tk.IntVar(value=cv2.FONT_HERSHEY_SIMPLEX)
        
        # Title
        ttk.Label(top_frame, text="Add Text", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Preview canvas
        h, w = image.shape[:2]
        scale = min(500/w, 300/h)
        preview_w, preview_h = int(w*scale), int(h*scale)
        
        canvas = tk.Canvas(preview_frame, width=preview_w, height=preview_h, bg="lightgray", bd=1, relief=tk.SOLID)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls
        controls_grid = ttk.Frame(controls_frame)
        controls_grid.pack(fill=tk.X, padx=5, pady=5)
        
        # Text input
        ttk.Label(controls_grid, text="Text:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(controls_grid, textvariable=text, width=30).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Position
        ttk.Label(controls_grid, text="Position:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        pos_frame = ttk.Frame(controls_grid)
        pos_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(pos_frame, textvariable=pos_x, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(pos_frame, textvariable=pos_y, width=5).pack(side=tk.LEFT, padx=2)
        
        # Font scale
        ttk.Label(controls_grid, text="Font Scale:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        scale_frame = ttk.Frame(controls_grid)
        scale_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Scale(scale_frame, from_=0.1, to=5.0, variable=font_scale, orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=2)
        ttk.Label(scale_frame, textvariable=font_scale).pack(side=tk.LEFT, padx=2)
        
        # Thickness
        ttk.Label(controls_grid, text="Thickness:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        thickness_frame = ttk.Frame(controls_grid)
        thickness_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Scale(thickness_frame, from_=1, to=10, variable=thickness, orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=2)
        ttk.Label(thickness_frame, textvariable=thickness).pack(side=tk.LEFT, padx=2)
        
        # Font face
        ttk.Label(controls_grid, text="Font:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        font_frame = ttk.Frame(controls_grid)
        font_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        fonts = [
            ("Simplex", cv2.FONT_HERSHEY_SIMPLEX),
            ("Plain", cv2.FONT_HERSHEY_PLAIN),
            ("Duplex", cv2.FONT_HERSHEY_DUPLEX),
            ("Complex", cv2.FONT_HERSHEY_COMPLEX),
            ("Triplex", cv2.FONT_HERSHEY_TRIPLEX),
            ("Complex Small", cv2.FONT_HERSHEY_COMPLEX_SMALL),
            ("Script Simplex", cv2.FONT_HERSHEY_SCRIPT_SIMPLEX),
            ("Script Complex", cv2.FONT_HERSHEY_SCRIPT_COMPLEX)
        ]
        
        font_combo = ttk.Combobox(font_frame, width=20, state="readonly")
        font_combo['values'] = [name for name, _ in fonts]
        font_combo.current(0)  # Set to first font
        font_combo.pack(side=tk.LEFT, padx=2)
        
        def font_selected(event):
            selected_name = font_combo.get()
            for name, value in fonts:
                if name == selected_name:
                    font_face.set(value)
                    update_preview()
                    break
        
        font_combo.bind("<<ComboboxSelected>>", font_selected)
        
        # Color
        ttk.Label(controls_grid, text="Color:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        color_frame = ttk.Frame(controls_grid)
        color_frame.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        color_preview = tk.Canvas(color_frame, width=20, height=20, bg=color.get())
        color_preview.pack(side=tk.LEFT, padx=2)
        
        def choose_color():
            rgb_color = colorchooser.askcolor(color.get())
            if rgb_color[1]:
                color.set(rgb_color[1])
                color_preview.config(bg=rgb_color[1])
                update_preview()
        
        ttk.Button(color_frame, text="Select Color", command=choose_color).pack(side=tk.LEFT, padx=2)
        
        # Update preview function
        def update_preview(*args):
            # Convert hex color to BGR
            hex_color = color.get().lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            bgr_color = (b, g, r)
            
            # Draw text on copy
            img_copy = image.copy()
            
            cv2.putText(img_copy, 
                      text.get(), 
                      (pos_x.get(), pos_y.get()), 
                      font_face.get(), 
                      font_scale.get(), 
                      bgr_color, 
                      thickness.get(),
                      cv2.LINE_AA)
            
            # Scale and display
            preview_img = cv2.resize(img_copy, (preview_w, preview_h))
            
            # Convert to RGB for Tkinter
            if len(preview_img.shape) == 2:  # Grayscale
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_GRAY2RGB)
            else:  # BGR
                preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB)
            
            try:
                # === SỬA PIL IMPORT ===
                img = self.Image.fromarray(preview_rgb)
                img_tk = self.ImageTk.PhotoImage(img)
                # ======================
                
                canvas.delete("all")
                canvas.create_image(preview_w//2, preview_h//2, image=img_tk)
                canvas.image = img_tk
            except Exception as e:
                # If PIL not available, just show a message
                canvas.delete("all")
                canvas.create_text(preview_w//2, preview_h//2, text=f"Preview error: {e}")
        
        # Register trace callbacks
        text.trace("w", update_preview)
        pos_x.trace("w", update_preview)
        pos_y.trace("w", update_preview)
        font_scale.trace("w", update_preview)
        thickness.trace("w", update_preview)
        color.trace("w", update_preview)
        font_face.trace("w", update_preview)
        
        # Update preview initially
        update_preview()
        
        # Action buttons
        def apply_text():
            nonlocal result
            try:
                # Convert hex color to BGR
                hex_color = color.get().lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                bgr_color = (b, g, r)
                
                new_img = image.copy()
                
                # Get font name for code comment
                font_name = next(name for name, val in fonts if val == font_face.get())
                
                cv2.putText(new_img, 
                          text.get(), 
                          (pos_x.get(), pos_y.get()), 
                          font_face.get(), 
                          font_scale.get(), 
                          bgr_color, 
                          thickness.get(),
                          cv2.LINE_AA)
                
                result = (new_img, f'cv2.putText(image, "{text.get()}", ({pos_x.get()}, {pos_y.get()}), cv2.FONT_HERSHEY_{font_name.upper().replace(" ", "_")}, fontScale={font_scale.get()}, color={bgr_color}, thickness={thickness.get()}, lineType=cv2.LINE_AA)  # Text: {text.get()}\n')
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add text: {str(e)}")
        
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_text).pack(side=tk.RIGHT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        return result

