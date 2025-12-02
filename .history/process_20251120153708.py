import cv2
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import numpy as np


class FunctionsProcessing:
    """
    Image Processing Functions Handler
    
    This class provides various image processing operations including:
    - Color space conversions (RGB, HSV, Grayscale)
    - Geometric transformations (resize, flip, rotate, move, perspective)
    - Filters and enhancement (blur, contrast, histogram equalization)
    - Segmentation and edge detection (thresholding, Canny)
    - Morphological operations (erode, dilate, open, close)
    - Intensity transformations (log, power/gamma)
    - Advanced operations (registration, stitching)
    - Drawing utilities (line, rectangle, circle, text)
    
    All operations return a tuple of (processed_image, code_string) where
    code_string contains the OpenCV code to reproduce the operation.
    """
    
    # === INITIALIZATION ===
    def __init__(self, pil_image_module, pil_image_tk_module):
        """
        Initialize with PIL modules via dependency injection.
        
        Args:
            pil_image_module: PIL.Image module
            pil_image_tk_module: PIL.ImageTk module
        """
        self.Image = pil_image_module
        self.ImageTk = pil_image_tk_module

    # ========================================================================
    # COLOR SPACE CONVERSIONS
    # ========================================================================
    
    def cvt_Negative(self, image):
        """Convert to Negative image color space."""
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "cv2.cvtColor(image, cv2.COLOR_BGR2RGB)\n"

    def cvt_HSV(self, image):
        """Convert BGR to HSV color space."""
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV), "cv2.cvtColor(image, cv2.COLOR_BGR2HSV)\n"

    def cvt_GRAY(self, image):
        """Convert BGR to Grayscale."""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), "cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
    
    # ========================================================================
    # FILTERS & ENHANCEMENT
    # ========================================================================
    
    def equalized_image(self, image):
        """Apply histogram equalization to enhance contrast."""
        # Check if image is grayscale
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            equalized = cv2.equalizeHist(gray)
            return equalized, "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\nequalized = cv2.equalizeHist(gray)\n"
        else:
            try:
                return cv2.equalizeHist(image), "equalized = cv2.equalizeHist(image)\n"
            except Exception:
                messagebox.showerror("Error", "Failed to equalize histogram. Image format not supported.")
                return None

    # ========================================================================
    # GEOMETRIC TRANSFORMATIONS
    # ========================================================================
    
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

    # ========================================================================
    # SEGMENTATION & EDGE DETECTION
    # ========================================================================
    
    def threshold_image(self, image):
        """Apply global thresholding with interactive preview."""
        # Check if image is grayscale
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            conversion_note = "# Convert to grayscale first\ngray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
        else:
            gray = image
            conversion_note = ""

        result = None
        dialog = tk.Toplevel()
        dialog.title("Global Threshold") # <-- Đổi tên
        dialog.geometry("800x800")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # ... (Phần còn lại của hàm không đổi, ngoại trừ việc sửa PIL) ...
        # Variables for threshold settings allaway int values

        thresh_value = tk.IntVar(value=127)
        max_value = tk.IntVar(value=255)
        thresh_type = tk.IntVar(value=cv2.THRESH_BINARY)
        
        # Display frames
        top_frame = ttk.Frame(dialog)
        top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Preview images (original grayscale and thresholded)
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Controls frame
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Type selection frame
        type_frame = ttk.Frame(dialog)
        type_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Title label
        ttk.Label(top_frame, text="Global Image Thresholding", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Create preview canvases
        ttk.Label(preview_frame, text="Original Grayscale:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(preview_frame, text="Thresholded:").grid(row=0, column=1, padx=5, pady=5)
        
        orig_canvas = tk.Canvas(preview_frame, width=350, height=200, bg="lightgray", bd=1, relief=tk.SOLID)
        orig_canvas.grid(row=1, column=0, padx=10, pady=5)
        
        thresh_canvas = tk.Canvas(preview_frame, width=350, height=200, bg="lightgray", bd=1, relief=tk.SOLID)
        thresh_canvas.grid(row=1, column=1, padx=10, pady=5)
        
        # Create controls
        ttk.Label(controls_frame, text="Threshold Value:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        thresh_scale = ttk.Scale(controls_frame, from_=0, to=255, variable=thresh_value, orient=tk.HORIZONTAL, length=300) # thresh_value là IntVar
        thresh_scale.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(controls_frame, textvariable=thresh_value).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Max Value:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        max_scale = ttk.Scale(controls_frame, from_=0, to=255, variable=max_value, orient=tk.HORIZONTAL, length=300)
        max_scale.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(controls_frame, textvariable=max_value).grid(row=1, column=2, padx=5, pady=5)
        
        controls_frame.columnconfigure(1, weight=1) # Make slider fill space
        
        # Threshold types
        thresh_types = [
            ("Binary", cv2.THRESH_BINARY),
            ("Binary Inverted", cv2.THRESH_BINARY_INV),
            ("Truncate", cv2.THRESH_TRUNC),
            ("To Zero", cv2.THRESH_TOZERO),
            ("To Zero Inverted", cv2.THRESH_TOZERO_INV),
            ("Otsu", cv2.THRESH_BINARY + cv2.THRESH_OTSU), # Thêm Otsu
        ]
        
        ttk.Label(type_frame, text="Threshold Type:").pack(anchor=tk.W)
        
        types_row_frame1 = ttk.Frame(type_frame)
        types_row_frame1.pack(fill=tk.X, pady=2)
        types_row_frame2 = ttk.Frame(type_frame)
        types_row_frame2.pack(fill=tk.X, pady=2)
        
        for i, (text, mode) in enumerate(thresh_types):
            frame = types_row_frame1 if i < 3 else types_row_frame2
            ttk.Radiobutton(frame, text=text, variable=thresh_type, value=mode).pack(side=tk.LEFT, padx=5)
        
        # Update preview function
        def update_preview(*args):
            # Get current values
            threshold = thresh_value.get()
            maxval = max_value.get()
            thtype = thresh_type.get()

            # Disable thresh_scale if Otsu is selected
            if thtype & cv2.THRESH_OTSU:
                thresh_scale.config(state="disabled")
            else:
                thresh_scale.config(state="normal")
            
            # Apply threshold
            ret, thresholded = cv2.threshold(gray, threshold, maxval, thtype)
            
            # If Otsu, update the slider to show the threshold it found
            if thtype & cv2.THRESH_OTSU:
                thresh_value.set(int(ret))
            
            # Display original gray image
            h, w = gray.shape[:2]
            scale = min(350/w, 200/h)
            dim = (int(w*scale), int(h*scale))
            gray_small = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
            
            # === SỬA PIL IMPORT ===
            img1 = self.Image.fromarray(gray_small)
            img1_tk = self.ImageTk.PhotoImage(img1)
            # ======================
            
            orig_canvas.delete("all")
            orig_canvas.create_image(175, 100, image=img1_tk) # Center in canvas
            orig_canvas.image = img1_tk
            
            # Display thresholded image
            thresh_small = cv2.resize(thresholded, dim, interpolation=cv2.INTER_AREA)
            
            # === SỬA PIL IMPORT ===
            img2 = self.Image.fromarray(thresh_small)
            img2_tk = self.ImageTk.PhotoImage(img2)
            # ======================
            
            thresh_canvas.delete("all")
            thresh_canvas.create_image(175, 100, image=img2_tk) # Center in canvas
            thresh_canvas.image = img2_tk
        
        # Register callbacks
        thresh_value.trace("w", update_preview)
        max_value.trace("w", update_preview)
        thresh_type.trace("w", update_preview)
        
        try:
            # === SỬA PIL IMPORT ===
            # Không cần import PIL ở đây nữa
            # ======================
            
            # Initial preview update
            update_preview()
            
            def threshold_ok():
                nonlocal result
                try:
                    threshold = thresh_value.get()
                    maxval = max_value.get()
                    thtype = thresh_type.get()
                    
                    # Apply threshold
                    ret, thresholded = cv2.threshold(gray, threshold, maxval, thtype)
                    
                    # Get threshold type name for code comment
                    type_name = "Otsu" if thtype & cv2.THRESH_OTSU else next(name for name, val in thresh_types if val == thtype)
                    thresh_val_str = "0" if thtype & cv2.THRESH_OTSU else str(threshold) # Use 0 for thresh if Otsu
                    type_val_str = "cv2.THRESH_BINARY + cv2.THRESH_OTSU" if thtype & cv2.THRESH_OTSU else f"cv2.THRESH_{type_name.upper().replace(' ', '_')}"
                    
                    result = (thresholded, f"{conversion_note}ret, thresholded = cv2.threshold(gray, {thresh_val_str}, {maxval}, {type_val_str})  # {type_name} threshold\n")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to apply threshold: {str(e)}")
            
            ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
            ttk.Button(buttons_frame, text="Apply", command=threshold_ok).pack(side=tk.RIGHT, padx=5)
            
            # Wait for dialog to close
            dialog.wait_window()
            return result
            
        except Exception as e: # Bắt lỗi chung
            # Fall back to simple dialog if PIL fails (dù đã sửa)
            messagebox.showerror("Preview Error", f"Failed to create preview: {e}")
            dialog.destroy()
            return self._simple_threshold_dialog(image, gray, conversion_note)
            
    def _simple_threshold_dialog(self, image, gray, conversion_note):
        # ... (Code của bạn không đổi, giữ nguyên logic) ...
        result = None
        new_window = tk.Toplevel()
        new_window.title("Threshold Settings")

        tk.Label(new_window, font=("Arial", 12), text="Threshold value (0-255):").pack()
        entry1 = tk.Entry(new_window, font=("Arial", 12))
        entry1.insert(0, "127")
        entry1.pack(pady=10)

        tk.Label(new_window, font=("Arial", 12), text="Max value (0-255):").pack()
        entry2 = tk.Entry(new_window, font=("Arial", 12))
        entry2.insert(0, "255")
        entry2.pack(pady=10)

        def get_value():
            nonlocal result
            try:
                thresh = float(entry1.get())
                maxval = float(entry2.get())

                if not (0 <= thresh <= 255) or not (0 <= maxval <= 255):
                    messagebox.showerror("Error", "Threshold and max values must be between 0-255.")
                    return

                ret, thresholded_image = cv2.threshold(gray, thresh, maxval, cv2.THRESH_BINARY)
                result = (thresholded_image, f"{conversion_note}ret, thresholded = cv2.threshold(gray, {thresh}, {maxval}, cv2.THRESH_BINARY)\n")
                new_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")

        button = tk.Button(new_window, text="Apply", command=get_value)
        button.pack(pady=10)
        new_window.wait_window()
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

    def perspective(self, image):
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

    def put_Text(self, image):
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

    # ========================================================================
    # HELPER FUNCTIONS FOR DIALOGS
    # ========================================================================
    
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

    def _update_preview_canvas(self, canvas, image, original_image):
        """Update canvas with resized image for preview.
        
        Args:
            canvas: Canvas widget to update
            image: Image to display (BGR or grayscale)
            original_image: Original image for scaling reference
        """
        try:
            h, w = original_image.shape[:2]
            canvas_w = canvas.winfo_width()
            canvas_h = canvas.winfo_height()
            
            if canvas_w < 2 or canvas_h < 2: # Canvas chưa được vẽ
                canvas_w, canvas_h = 500, 300 # Giá trị tạm
                
            scale = min(canvas_w/w, canvas_h/h)
            preview_w, preview_h = int(w*scale), int(h*scale)
            
            resized_img = cv2.resize(image, (preview_w, preview_h), interpolation=cv2.INTER_AREA)
            
            if len(resized_img.shape) == 2:
                img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_GRAY2RGB)
            else:
                img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
                
            img_tk = self.ImageTk.PhotoImage(self.Image.fromarray(img_rgb))
            canvas.delete("all")
            canvas.create_image(canvas_w//2, canvas_h//2, image=img_tk)
            canvas.image = img_tk
        except Exception as e:
            canvas.delete("all")
            canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2, text=f"Preview error: {e}", fill="red")

    # ========================================================================
    # BLUR & NOISE REDUCTION DIALOGS
    # ========================================================================
    
    def gaussian_blur_dialog(self, image):
        """Apply Gaussian blur with adjustable kernel size."""
        result = None
        dialog, canvas, controls, buttons = self._create_basic_preview_dialog("Gaussian Blur")
        
        k_size = tk.IntVar(value=5)
        
        # Controls
        ttk.Label(controls, text="Kernel Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        k_scale = ttk.Scale(controls, from_=1, to=51, variable=k_size, orient=tk.HORIZONTAL, length=300)
        k_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        k_label = ttk.Label(controls, text="5x5", width=5)
        k_label.grid(row=0, column=2, padx=5)
        
        controls.columnconfigure(1, weight=1)
        
        def update_preview(*args):
            k = k_size.get()
            if k % 2 == 0: k += 1 # Kernel size phải là số lẻ
            k_label.config(text=f"{k}x{k}")
            
            try:
                blurred = cv2.GaussianBlur(image, (k, k), 0)
                self._update_preview_canvas(canvas, blurred, image)
            except Exception as e:
                canvas.delete("all")
                canvas.create_text(250, 150, text=str(e), fill="red")
        
        k_size.trace("w", update_preview)
        
        def apply_blur():
            nonlocal result
            k = k_size.get()
            if k % 2 == 0: k += 1
            blurred = cv2.GaussianBlur(image, (k, k), 0)
            result = (blurred, f"blurred = cv2.GaussianBlur(image, ({k}, {k}), 0)\n")
            dialog.destroy()
            
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons, text="Apply", command=apply_blur).pack(side=tk.RIGHT, padx=5)
        
        dialog.after(100, update_preview) # Cập nhật preview ban đầu
        dialog.wait_window()
        return result
        
    def median_blur_dialog(self, image):
        """Apply median blur for salt-and-pepper noise reduction."""
        result = None
        dialog, canvas, controls, buttons = self._create_basic_preview_dialog("Median Blur")
        
        k_size = tk.IntVar(value=5)
        
        # Controls
        ttk.Label(controls, text="Kernel Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        k_scale = ttk.Scale(controls, from_=1, to=51, variable=k_size, orient=tk.HORIZONTAL, length=300)
        k_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        k_label = ttk.Label(controls, text="5x5", width=5)
        k_label.grid(row=0, column=2, padx=5)
        
        controls.columnconfigure(1, weight=1)
        
        def update_preview(*args):
            k = k_size.get()
            if k % 2 == 0: k += 1 # Kernel size phải là số lẻ
            k_label.config(text=f"{k}x{k}")
            
            try:
                blurred = cv2.medianBlur(image, k)
                self._update_preview_canvas(canvas, blurred, image)
            except Exception as e:
                canvas.delete("all")
                canvas.create_text(250, 150, text=str(e), fill="red")
        
        k_size.trace("w", update_preview)
        
        def apply_blur():
            nonlocal result
            k = k_size.get()
            if k % 2 == 0: k += 1
            blurred = cv2.medianBlur(image, k)
            result = (blurred, f"blurred = cv2.medianBlur(image, {k})\n")
            dialog.destroy()
            
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons, text="Apply", command=apply_blur).pack(side=tk.RIGHT, padx=5)
        
        dialog.after(100, update_preview) # Cập nhật preview ban đầu
        dialog.wait_window()
        return result

    # ========================================================================
    # MORPHOLOGICAL OPERATIONS
    # ========================================================================
    
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

    def adaptive_threshold_dialog(self, image):
        """Apply adaptive thresholding with preview dialog."""
        # Check if image is grayscale
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            conversion_note = "# Convert to grayscale first\ngray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
        else:
            gray = image
            conversion_note = ""

        result = None
        dialog = tk.Toplevel()
        dialog.title("Adaptive Threshold")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Variables
        method_var = tk.IntVar(value=cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        thresh_type = tk.IntVar(value=cv2.THRESH_BINARY)
        block_size = tk.IntVar(value=11)
        c_value = tk.IntVar(value=2)

        # Create preview
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(preview_frame, text="Original:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(preview_frame, text="Result:").grid(row=0, column=1, padx=5, pady=5)

        orig_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        orig_canvas.grid(row=1, column=0, padx=10, pady=5)

        result_canvas = tk.Canvas(preview_frame, width=350, height=250, bg="lightgray")
        result_canvas.grid(row=1, column=1, padx=10, pady=5)

        # Controls
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(controls_frame, text="Method:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(controls_frame, text="Mean", variable=method_var, 
                       value=cv2.ADAPTIVE_THRESH_MEAN_C).grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(controls_frame, text="Gaussian", variable=method_var, 
                       value=cv2.ADAPTIVE_THRESH_GAUSSIAN_C).grid(row=0, column=2, sticky=tk.W)

        ttk.Label(controls_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(controls_frame, text="Binary", variable=thresh_type, 
                       value=cv2.THRESH_BINARY).grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(controls_frame, text="Binary Inv", variable=thresh_type, 
                       value=cv2.THRESH_BINARY_INV).grid(row=1, column=2, sticky=tk.W)

        ttk.Label(controls_frame, text="Block Size:").grid(row=2, column=0, sticky=tk.W, pady=5)
        block_scale = ttk.Scale(controls_frame, from_=3, to=51, variable=block_size, orient=tk.HORIZONTAL, length=300)
        block_scale.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=5)
        ttk.Label(controls_frame, textvariable=block_size).grid(row=2, column=3, padx=5)

        ttk.Label(controls_frame, text="C Value:").grid(row=3, column=0, sticky=tk.W, pady=5)
        c_scale = ttk.Scale(controls_frame, from_=-10, to=10, variable=c_value, orient=tk.HORIZONTAL, length=300)
        c_scale.grid(row=3, column=1, columnspan=2, sticky=tk.EW, pady=5)
        ttk.Label(controls_frame, textvariable=c_value).grid(row=3, column=3, padx=5)

        def update_preview(*args):
            bs = block_size.get()
            if bs % 2 == 0:
                bs += 1
                block_size.set(bs)
            
            adaptive = cv2.adaptiveThreshold(gray, 255, method_var.get(), thresh_type.get(), bs, c_value.get())
            self._update_preview_canvas(orig_canvas, gray, gray)
            self._update_preview_canvas(result_canvas, adaptive, gray)

        def apply_adaptive():
            nonlocal result
            bs = block_size.get()
            if bs % 2 == 0:
                bs += 1
            adaptive = cv2.adaptiveThreshold(gray, 255, method_var.get(), thresh_type.get(), bs, c_value.get())
            
            method_name = "ADAPTIVE_THRESH_MEAN_C" if method_var.get() == cv2.ADAPTIVE_THRESH_MEAN_C else "ADAPTIVE_THRESH_GAUSSIAN_C"
            type_name = "THRESH_BINARY" if thresh_type.get() == cv2.THRESH_BINARY else "THRESH_BINARY_INV"
            
            code = conversion_note
            code += f"# Apply adaptive threshold\n"
            code += f"result = cv2.adaptiveThreshold(gray, 255, cv2.{method_name}, cv2.{type_name}, {bs}, {c_value.get()})\n"
            result = (adaptive, code)
            dialog.destroy()

        method_var.trace("w", update_preview)
        thresh_type.trace("w", update_preview)
        block_size.trace("w", update_preview)
        c_value.trace("w", update_preview)

        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_adaptive).pack(side=tk.RIGHT, padx=5)

        update_preview()
        dialog.wait_window()
        return result

    # --- CONTRAST & INTENSITY TRANSFORMATIONS ---
    
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

    # --- ADVANCED: REGISTRATION & STITCHING ---
    
    def image_registration_dialog(self, image):
        """Register two images using feature matching."""
        from tkinter import filedialog
        
        # Let user select reference image
        ref_path = filedialog.askopenfilename(
            title="Select Reference Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        
        if not ref_path:
            return None
        
        reference = cv2.imread(ref_path)
        if reference is None:
            messagebox.showerror("Error", "Failed to load reference image")
            return None
        
        result = None
        dialog = tk.Toplevel()
        dialog.title("Image Registration")
        dialog.geometry("900x700")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Variables
        method_var = tk.StringVar(value="orb")
        match_threshold = tk.DoubleVar(value=0.75)

        # Preview
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(preview_frame, text="Reference:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(preview_frame, text="Moving:").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(preview_frame, text="Registered:").grid(row=0, column=2, padx=5, pady=5)

        ref_canvas = tk.Canvas(preview_frame, width=280, height=200, bg="lightgray")
        ref_canvas.grid(row=1, column=0, padx=5, pady=5)

        moving_canvas = tk.Canvas(preview_frame, width=280, height=200, bg="lightgray")
        moving_canvas.grid(row=1, column=1, padx=5, pady=5)

        result_canvas = tk.Canvas(preview_frame, width=280, height=200, bg="lightgray")
        result_canvas.grid(row=1, column=2, padx=5, pady=5)

        # Controls
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(controls_frame, text="Feature Detector:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(controls_frame, text="ORB", variable=method_var, value="orb").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(controls_frame, text="SIFT", variable=method_var, value="sift").grid(row=0, column=2, sticky=tk.W)

        ttk.Label(controls_frame, text="Match Ratio:").grid(row=1, column=0, sticky=tk.W, pady=5)
        threshold_scale = ttk.Scale(controls_frame, from_=0.5, to=0.95, variable=match_threshold, 
                                    orient=tk.HORIZONTAL, length=300)
        threshold_scale.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=5)
        ttk.Label(controls_frame, textvariable=match_threshold, width=6).grid(row=1, column=3, padx=5)

        info_label = ttk.Label(controls_frame, text="", foreground="blue")
        info_label.grid(row=2, column=0, columnspan=4, pady=10)

        def perform_registration():
            try:
                # Convert to grayscale
                ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
                moving_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect features
                if method_var.get() == "orb":
                    detector = cv2.ORB_create(nfeatures=5000)
                    kp1, des1 = detector.detectAndCompute(ref_gray, None)
                    kp2, des2 = detector.detectAndCompute(moving_gray, None)
                    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
                else:  # SIFT
                    detector = cv2.SIFT_create()
                    kp1, des1 = detector.detectAndCompute(ref_gray, None)
                    kp2, des2 = detector.detectAndCompute(moving_gray, None)
                    matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

                # Match features
                matches = matcher.knnMatch(des2, des1, k=2)
                
                # Apply ratio test
                good_matches = []
                for match_pair in matches:
                    if len(match_pair) == 2:
                        m, n = match_pair
                        if m.distance < match_threshold.get() * n.distance:
                            good_matches.append(m)

                info_label.config(text=f"Found {len(good_matches)} good matches")

                if len(good_matches) < 4:
                    return None, "Not enough matches found"

                # Extract matched points
                src_pts = np.float32([kp2[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp1[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                # Find homography
                H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                if H is None:
                    return None, "Failed to compute homography"

                # Warp image
                h, w = reference.shape[:2]
                registered = cv2.warpPerspective(image, H, (w, h))

                return registered, None

            except Exception as e:
                return None, str(e)

        def update_preview(*args):
            registered, error = perform_registration()
            
            self._update_preview_canvas(ref_canvas, reference, reference)
            self._update_preview_canvas(moving_canvas, image, image)
            
            if registered is not None:
                self._update_preview_canvas(result_canvas, registered, reference)
            else:
                info_label.config(text=f"Error: {error}", foreground="red")

        def apply_registration():
            nonlocal result
            registered, error = perform_registration()
            
            if registered is not None:
                method_name = method_var.get().upper()
                code = f"# Image registration using {method_name}\n"
                code += f"import numpy as np\n"
                code += f"ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)\n"
                code += f"moving_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n"
                
                if method_var.get() == "orb":
                    code += f"detector = cv2.ORB_create(nfeatures=5000)\n"
                    code += f"matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)\n"
                else:
                    code += f"detector = cv2.SIFT_create()\n"
                    code += f"matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)\n"
                
                code += f"kp1, des1 = detector.detectAndCompute(ref_gray, None)\n"
                code += f"kp2, des2 = detector.detectAndCompute(moving_gray, None)\n"
                code += f"matches = matcher.knnMatch(des2, des1, k=2)\n\n"
                code += f"good_matches = [m for m, n in matches if m.distance < {match_threshold.get():.2f} * n.distance]\n"
                code += f"src_pts = np.float32([kp2[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)\n"
                code += f"dst_pts = np.float32([kp1[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)\n"
                code += f"H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)\n"
                code += f"h, w = reference.shape[:2]\n"
                code += f"registered = cv2.warpPerspective(image, H, (w, h))\n"
                
                result = (registered, code)
                dialog.destroy()
            else:
                messagebox.showerror("Error", f"Registration failed: {error}")

        method_var.trace("w", update_preview)
        match_threshold.trace("w", update_preview)

        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Apply", command=apply_registration).pack(side=tk.RIGHT, padx=5)

        update_preview()
        dialog.wait_window()
        return result

    def image_stitching_dialog(self, image):
        """Stitch multiple images together to create panorama."""
        from tkinter import filedialog
        
        # Let user select additional images
        file_paths = filedialog.askopenfilenames(
            title="Select Images to Stitch (in order)",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        
        if not file_paths:
            return None
        
        # Load all images
        images = [image]  # Start with current image
        for path in file_paths:
            img = cv2.imread(path)
            if img is not None:
                images.append(img)
        
        if len(images) < 2:
            messagebox.showinfo("Info", "Need at least 2 images to stitch")
            return None
        
        result = None
        dialog = tk.Toplevel()
        dialog.title("Image Stitching")
        dialog.geometry("900x700")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Variables
        mode_var = tk.StringVar(value="panorama")

        # Preview area with scrolling
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(preview_frame, text=f"Stitching {len(images)} images...").pack(pady=5)

        # Canvas for result
        canvas_frame = ttk.Frame(preview_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        result_canvas = tk.Canvas(canvas_frame, width=850, height=400, bg="lightgray")
        result_canvas.pack(fill=tk.BOTH, expand=True)

        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=result_canvas.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        result_canvas.configure(xscrollcommand=h_scroll.set)

        # Controls
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(controls_frame, text="Stitch Mode:").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(controls_frame, text="Panorama", variable=mode_var, value="panorama").pack(anchor=tk.W)
        ttk.Radiobutton(controls_frame, text="Scans", variable=mode_var, value="scans").pack(anchor=tk.W)

        info_label = ttk.Label(controls_frame, text="", foreground="blue")
        info_label.pack(pady=10)

        progress_label = ttk.Label(controls_frame, text="")
        progress_label.pack(pady=5)

        def perform_stitching():
            try:
                info_label.config(text="Processing...", foreground="blue")
                progress_label.config(text="Detecting features and matching...")
                dialog.update()

                # Create stitcher
                if mode_var.get() == "panorama":
                    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
                else:
                    stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)

                # Perform stitching
                status, panorama = stitcher.stitch(images)

                if status == cv2.Stitcher_OK:
                    info_label.config(text="Stitching successful!", foreground="green")
                    progress_label.config(text=f"Result size: {panorama.shape[1]}x{panorama.shape[0]}")
                    return panorama, None
                else:
                    error_msgs = {
                        cv2.Stitcher_ERR_NEED_MORE_IMGS: "Need more images",
                        cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Homography estimation failed",
                        cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Camera parameters adjustment failed"
                    }
                    error_msg = error_msgs.get(status, f"Stitching failed with status {status}")
                    info_label.config(text=error_msg, foreground="red")
                    return None, error_msg

            except Exception as e:
                error_msg = str(e)
                info_label.config(text=f"Error: {error_msg}", foreground="red")
                return None, error_msg

        def update_preview(*args):
            panorama, error = perform_stitching()
            
            if panorama is not None:
                # Display panorama
                h, w = panorama.shape[:2]
                scale = min(800 / w, 380 / h)
                display_w, display_h = int(w * scale), int(h * scale)
                
                resized = cv2.resize(panorama, (display_w, display_h))
                
                if len(resized.shape) == 2:
                    rgb = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
                else:
                    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                
                pil_img = self.Image.fromarray(rgb)
                photo = self.ImageTk.PhotoImage(pil_img)
                
                result_canvas.delete("all")
                result_canvas.create_image(0, 0, anchor='nw', image=photo)
                result_canvas.image = photo
                result_canvas.config(scrollregion=(0, 0, display_w, display_h))

        def apply_stitching():
            nonlocal result
            panorama, error = perform_stitching()
            
            if panorama is not None:
                mode_name = "PANORAMA" if mode_var.get() == "panorama" else "SCANS"
                code = f"# Image stitching\n"
                code += f"stitcher = cv2.Stitcher_create(cv2.Stitcher_{mode_name})\n"
                code += f"# images = [image1, image2, ...] # List of images to stitch\n"
                code += f"status, panorama = stitcher.stitch(images)\n"
                code += f"if status == cv2.Stitcher_OK:\n"
                code += f"    result = panorama\n"
                
                result = (panorama, code)
                dialog.destroy()
            else:
                messagebox.showerror("Error", f"Stitching failed: {error}")

        mode_var.trace("w", update_preview)

        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Stitch", command=apply_stitching).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Preview", command=update_preview).pack(side=tk.RIGHT, padx=5)

        dialog.wait_window()
        return result
        """Dialog mới cho Adaptive Threshold."""
        # Phải là ảnh xám
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            conversion_note = "# Convert to grayscale first\ngray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
        else:
            gray = image
            conversion_note = ""
            
        result = None
        dialog, canvas, controls, buttons = self._create_basic_preview_dialog("Adaptive Threshold", "700x650")
        
        # Variables
        block_size = tk.IntVar(value=11)
        c_value = tk.IntVar(value=2)
        adaptive_method = tk.IntVar(value=cv2.ADAPTIVE_THRESH_MEAN_C)
        threshold_type = tk.IntVar(value=cv2.THRESH_BINARY)
        
        # Controls
        # Adaptive Method
        method_frame = ttk.LabelFrame(controls, text="Adaptive Method")
        method_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(method_frame, text="Mean C", variable=adaptive_method, value=cv2.ADAPTIVE_THRESH_MEAN_C).pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Radiobutton(method_frame, text="Gaussian C", variable=adaptive_method, value=cv2.ADAPTIVE_THRESH_GAUSSIAN_C).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Threshold Type
        type_frame = ttk.LabelFrame(controls, text="Threshold Type")
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(type_frame, text="Binary", variable=threshold_type, value=cv2.THRESH_BINARY).pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Radiobutton(type_frame, text="Binary Inverted", variable=threshold_type, value=cv2.THRESH_BINARY_INV).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Block Size
        block_frame = ttk.Frame(controls)
        block_frame.pack(fill=tk.X, pady=5)
        ttk.Label(block_frame, text="Block Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        block_scale = ttk.Scale(block_frame, from_=3, to=255, variable=block_size, orient=tk.HORIZONTAL, length=300)
        block_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        block_label = ttk.Label(block_frame, text="11", width=5)
        block_label.grid(row=0, column=2, padx=5)
        block_frame.columnconfigure(1, weight=1)
        
        # C Value
        c_frame = ttk.Frame(controls)
        c_frame.pack(fill=tk.X, pady=5)
        ttk.Label(c_frame, text="Constant (C):").grid(row=0, column=0, sticky=tk.W, padx=5)
        c_scale = ttk.Scale(c_frame, from_=-50, to=50, variable=c_value, orient=tk.HORIZONTAL, length=300)
        c_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        c_label = ttk.Label(c_frame, textvariable=c_value, width=5)
        c_label.grid(row=0, column=2, padx=5)
        c_frame.columnconfigure(1, weight=1)
        
        def update_preview(*args):
            b = block_size.get()
            if b % 2 == 0: b += 1 # Block size phải là số lẻ
            if b < 3: b = 3       # Block size phải >= 3
            block_label.config(text=str(b))
            
            c = c_value.get()
            method = adaptive_method.get()
            ttype = threshold_type.get()
            
            try:
                thresholded = cv2.adaptiveThreshold(gray, 255, method, ttype, b, c)
                self._update_preview_canvas(canvas, thresholded, gray)
            except Exception as e:
                canvas.delete("all")
                canvas.create_text(250, 150, text=str(e), fill="red")
        
        block_size.trace("w", update_preview)
        c_value.trace("w", update_preview)
        adaptive_method.trace("w", update_preview)
        threshold_type.trace("w", update_preview)
        
        def apply_adaptive_thresh():
            nonlocal result
            b = block_size.get()
            if b % 2 == 0: b += 1
            if b < 3: b = 3
            
            c = c_value.get()
            method = adaptive_method.get()
            ttype = threshold_type.get()
            
            thresholded = cv2.adaptiveThreshold(gray, 255, method, ttype, b, c)
            
            method_name = "ADAPTIVE_THRESH_MEAN_C" if method == cv2.ADAPTIVE_THRESH_MEAN_C else "ADAPTIVE_THRESH_GAUSSIAN_C"
            type_name = "THRESH_BINARY" if ttype == cv2.THRESH_BINARY else "THRESH_BINARY_INV"
            
            code = f"{conversion_note}"
            code += f"thresholded = cv2.adaptiveThreshold(gray, 255, cv2.{method_name}, cv2.{type_name}, {b}, {c})\n"
            
            result = (thresholded, code)
            dialog.destroy()
            
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons, text="Apply", command=apply_adaptive_thresh).pack(side=tk.RIGHT, padx=5)
        
        dialog.after(100, update_preview) # Cập nhật preview ban đầu
        dialog.wait_window()
        return result