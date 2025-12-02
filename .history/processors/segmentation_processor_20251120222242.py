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
