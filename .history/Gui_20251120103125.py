from tkinter import filedialog, ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk  # <-- Import PIL ở đây
from process import FunctionsProcessing # <-- Thay đổi import
import os
import cv2

class GUI:
    def __init__(self, root):
        self.file_path = None
        self.display_Image = None
        self.original_image = None
        self.canvas = None
        self.scale = None
        self.functions = None
        self.transformation = StringVar(value="Grayscale")
        self.code_text = ""
        self.history = []
        self.history_position = -1
        self.set_code_text = StringVar(value="")
        
        # === CẢI TIẾN QUAN TRỌNG: Dependency Injection ===
        # Khởi tạo PIL và truyền vào class processing
        # Điều này giúp processing.py không phụ thuộc vào PIL
        self.pil_image_module = Image
        self.pil_image_tk_module = ImageTk
        self.fp = FunctionsProcessing(self.pil_image_module, self.pil_image_tk_module)
        # =================================================
        
        self.root = root
        self.setUpGUI()
        
    def setUpGUI(self):
        self.root.title("Image Processing Studio")
        self.root.geometry("1450x800")
        self.root.configure(bg="#f0f0f0")
        
        # Configure styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Category.TLabel", font=("Arial", 12, "bold"), background="#f0f0f0", foreground="#333333")
        
        # Main frames
        top_frame = ttk.Frame(self.root, style="TFrame")
        top_frame.pack(fill=X, padx=10, pady=10)
        
        content_frame = ttk.Frame(self.root, style="TFrame")
        content_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Left panel for controls
        left_panel = ttk.Frame(content_frame, style="TFrame")
        left_panel.pack(side=LEFT, fill=Y, padx=5, pady=5)
        
        # Center panel for image
        center_panel = ttk.Frame(content_frame, style="TFrame")
        center_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        # Right panel for additional controls
        right_panel = ttk.Frame(content_frame, style="TFrame")
        right_panel.pack(side=RIGHT, fill=Y, padx=5, pady=5)
        
        # Bottom panel for code
        bottom_panel = ttk.Frame(self.root, style="TFrame")
        bottom_panel.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Top frame content - file operations
        ttk.Button(top_frame, text="Load Image", command=self.load_image).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Save Image", command=self.save_image).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Reset Image", command=self.reload_image).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Undo", command=self.undo).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Redo", command=self.redo).pack(side=LEFT, padx=5)
        
        # Image file info label
        self.file_info = ttk.Label(top_frame, text="No image loaded", font=("Arial", 10))
        self.file_info.pack(side=RIGHT, padx=10)
        
        # Image display
        image_frame = ttk.Frame(center_panel, style="TFrame")
        image_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # Fixed size canvas container with scrollbars
        canvas_container = ttk.Frame(image_frame)
        canvas_container.pack(fill=BOTH, expand=True)
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        
        # Canvas for image display with fixed size
        self.canvas = Canvas(canvas_container, width=900, height=500, bg="#dddddd", 
                            highlightthickness=1, highlightbackground="#999999")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbars to the canvas
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=VERTICAL, command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure the canvas
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Zoom controls
        zoom_frame = ttk.Frame(center_panel, style="TFrame")
        zoom_frame.pack(fill=X, pady=5)
        
        ttk.Label(zoom_frame, text="Zoom:", style="TLabel").pack(side=LEFT, padx=5)
        ttk.Button(zoom_frame, text="−", width=3, command=self.zoom_out).pack(side=LEFT, padx=2)
        self.zoom_label = ttk.Label(zoom_frame, text="100%", width=8)
        self.zoom_label.pack(side=LEFT, padx=5)
        ttk.Button(zoom_frame, text="+", width=3, command=self.zoom_in).pack(side=LEFT, padx=2)
        ttk.Button(zoom_frame, text="Fit", width=5, command=self.zoom_fit).pack(side=LEFT, padx=5)
        ttk.Button(zoom_frame, text="100%", width=5, command=self.zoom_reset).pack(side=LEFT, padx=5)
        
        # === CẬP NHẬT GIAO DIỆN ===
        
        # Function categories in left and right panels
        self.create_function_category(left_panel, "Color Conversions", [
            ("BGR to RGB", "BGR to RGB"),
            ("BGR to Gray", "BGR to Gray"),
            ("BGR to HSV", "BGR to HSV"),
        ])
        
        self.create_function_category(left_panel, "Geometric Transformations", [
            ("Resize", "Resize"),
            ("Flip", "Flip"),
            ("Rotate 90°", "Rotate_90"),
            ("Rotate Custom", "Rotate Matrix"),
            ("Move", "Move"),
            ("Perspective", "Perspective"),
        ])
        self.create_function_category(left_panel, "Intensity Transform", [
                    ("Log Transform", "Log Transform"),
                    ("Power Transform (Gamma)", "Power Transform"),
                ])
        # Nhóm mới cho Hình thái học
        self.create_function_category(left_panel, "Morphological Ops", [
            ("E | D | O | C", "Morphology"),
        ])
        
        # Sắp xếp lại các nhóm bên phải
        self.create_function_category(right_panel, "Segmentation & Edge", [
            ("Global Threshold", "Threshold"),
            ("Adaptive Threshold", "Adaptive Threshold"),
            ("Canny Edge", "Canny"),
        ])

        self.create_function_category(right_panel, "Filters & Enhancement", [
            ("Histogram Equalize", "Equalized"),
            ("Gaussian Blur", "GaussianBlur Dialog"),
            ("Median Blur", "MedianBlur Dialog"),
            ("Contrast Enhancement", "Contrast Enhancement"),
        ])
        
        
        
        self.create_function_category(right_panel, "Advanced Processing", [
            ("Image Registration", "Image Registration"),
            ("Image Stitching", "Image Stitching"),
        ])
        
        self.create_function_category(right_panel, "Drawing", [
            ("Draw Line", "Draw line"),
            ("Draw Rectangle", "Draw rectangle"),
            ("Draw Circle", "Draw circle"),
            ("Put Text", "Put text"),
        ])
        # ===========================
        
    
        
        # Set initial scale
        self.scale = 1.0
        
        # Add keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-r>", lambda e: self.reload_image())
        self.root.bind("<plus>", lambda e: self.zoom_in())
        self.root.bind("<minus>", lambda e: self.zoom_out())
        
    def create_function_category(self, parent, title, functions):
        """Create a category frame with buttons for image processing functions."""
        frame = ttk.Frame(parent, style="TFrame")
        frame.pack(fill=X, padx=5, pady=10)
        
        ttk.Label(frame, text=title, style="Category.TLabel").pack(anchor=W, pady=(0, 5))
        
        for label, transformation in functions:
            btn = ttk.Button(frame, text=label, width=28,
                          command=lambda t=transformation: self.apply_transformation(t))
            btn.pack(fill=X, pady=2)
    
    def update_code_display(self):
        self.code_display.delete("1.0", "end")
        self.code_display.insert("1.0", self.set_code_text.get())
    
    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if self.file_path:
            self.original_image = cv2.imread(self.file_path)
            self.display_Image = self.original_image.copy()
            self.code_text = f"# Load image\nimage = cv2.imread('{os.path.basename(self.file_path)}')\n"
            self.set_code_text.set(self.code_text)
            
            # Update file info
            img_h, img_w = self.display_Image.shape[:2]
            file_name = os.path.basename(self.file_path)
            self.file_info.config(text=f"{file_name} ({img_w}×{img_h})")
            
            # Reset history
            self.history = [(self.display_Image.copy(), self.code_text)]
            self.history_position = 0
            
            self.update_image()
    
    def save_image(self):
        if self.display_Image is None:
            messagebox.showinfo("Info", "No image to save")
            return
            
        save_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if save_path:
            cv2.imwrite(save_path, self.display_Image)
            messagebox.showinfo("Success", f"Image saved to {save_path}")
    
    def reload_image(self):
        if self.original_image is not None:
            self.display_Image = self.original_image.copy()
            self.scale = 1.0
            self.zoom_label.config(text="100%")
            self.code_text = f"# Load image\nimage = cv2.imread('{os.path.basename(self.file_path)}')\n"
            self.set_code_text.set(self.code_text)
            
            # Reset history
            self.history = [(self.display_Image.copy(), self.code_text)]
            self.history_position = 0
            
            self.update_image()
        else:
            messagebox.showinfo("Info", "No image loaded")
    
    def update_image(self):
        if self.display_Image is None:
            return
            
        # Scale the image
        h, w = self.display_Image.shape[:2]
        scaled_w, scaled_h = int(w * self.scale), int(h * self.scale)
        resized_image = cv2.resize(self.display_Image, (scaled_w, scaled_h))
        
        # Convert to RGB for display
        if len(resized_image.shape) == 2:  # Grayscale
            image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
        else:  # Color (BGR)
            image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            
        img = self.pil_image_module.fromarray(image_rgb)  # <-- Dùng module đã truyền
        img_tk = self.pil_image_tk_module.PhotoImage(img) # <-- Dùng module đã truyền
        
        # Update canvas
        self.canvas.delete("all")
        
        # Store the image object to prevent garbage collection
        self.current_image_tk = img_tk
        
        # Create image in the center of canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate position to center the image
        x_pos = max(0, (canvas_width - scaled_w) // 2)
        y_pos = max(0, (canvas_height - scaled_h) // 2)
        
        self.canvas.create_image(x_pos, y_pos, anchor='nw', image=self.current_image_tk)
        
        # Update scrollregion to encompass the image
        self.update_scrollregion()
    
    def zoom_in(self):
        self.scale *= 1.2
        self.zoom_label.config(text=f"{int(self.scale * 100)}%")
        self.update_image()
    
    def zoom_out(self):
        self.scale *= 0.8
        self.zoom_label.config(text=f"{int(self.scale * 100)}%")
        self.update_image()
    
    def zoom_reset(self):
        self.scale = 1.0
        self.zoom_label.config(text="100%")
        self.update_image()
    
    def zoom_fit(self):
        if self.display_Image is None:
            return
            
        # Calculate scale to fit image in canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_h, img_w = self.display_Image.shape[:2]
        
        scale_w = canvas_width / img_w
        scale_h = canvas_height / img_h
        self.scale = min(scale_w, scale_h) * 0.95  # 95% of fit scale for padding
        
        self.zoom_label.config(text=f"{int(self.scale * 100)}%")
        self.update_image()
    
    def undo(self):
        if self.history_position > 0:
            self.history_position -= 1
            self.display_Image, self.code_text = self.history[self.history_position]
            self.set_code_text.set(self.code_text)
            self.update_image()
    
    def redo(self):
        if self.history_position < len(self.history) - 1:
            self.history_position += 1
            self.display_Image, self.code_text = self.history[self.history_position]
            self.set_code_text.set(self.code_text)
            self.update_image()
    
    def apply_transformation(self, transformation):
        if self.display_Image is None:
            messagebox.showinfo("Info", "Please load an image first")
            return
            
        # === CẬP NHẬT FUNC_MAP ===
        func_map = {
            "BGR to RGB"    : self.fp.cvt_RGB     ,
            "BGR to Gray"   : self.fp.cvt_GRAY    ,
            "BGR to HSV"    : self.fp.cvt_HSV     ,
            "Resize"        : self.fp.resize_image,
            "Flip"          : self.fp.flip_image,
            "Rotate_90"     : self.fp.rotate_image,
            "Threshold"     : self.fp.threshold_image,
            "Equalized"     : self.fp.equalized_image,
            "Move"          : self.fp.move_image,
            "Rotate Matrix" : self.fp.rotationMatrix2d,
            "Perspective"   : self.fp.perspective,
            "Canny"         : self.fp.canny_detection,
            "Draw line"     : self.fp.draw_Line,
            "Draw rectangle": self.fp.draw_Rectangle,
            "Draw circle"   : self.fp.draw_Circle,
            "Put text"      : self.fp.put_Text,
            
            # CHỨC NĂNG ĐÃ CÓ - NÂNG CẤP
            "GaussianBlur Dialog" : self.fp.gaussian_blur_dialog,
            "MedianBlur Dialog"   : self.fp.median_blur_dialog,
            "Morphology"          : self.fp.morph_operations_dialog,
            "Adaptive Threshold"  : self.fp.adaptive_threshold_dialog,
            
            # CHỨC NĂNG MỚI
            "Contrast Enhancement": self.fp.contrast_enhancement_dialog,
            "Log Transform"       : self.fp.log_transform_dialog,
            "Power Transform"     : self.fp.power_transform_dialog,
            "Image Registration"  : self.fp.image_registration_dialog,
            "Image Stitching"     : self.fp.image_stitching_dialog,
        }
        # ===========================
        

        
        result = func_map[transformation](self.display_Image)
        if result:
            temp_image, code = result
            self.code_text += code
            self.display_Image = temp_image
            self.set_code_text.set(self.code_text)
            
            # Add to history
            self.history = self.history[:self.history_position+1]  # Truncate forward history
            self.history.append((self.display_Image.copy(), self.code_text))
            self.history_position = len(self.history) - 1
            
            self.update_image()
    
    def on_canvas_configure(self, event):
        # Update scrollregion when canvas is resized
        self.update_scrollregion()
    
    def update_scrollregion(self):
        # Update scrollregion to match image size at current scale
        if self.display_Image is not None:
            h, w = self.display_Image.shape[:2]
            scaled_w, scaled_h = int(w * self.scale), int(h * self.scale)
            
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Bbox is (left, top, right, bottom)
            x_pos = max(0, (canvas_width - scaled_w) // 2)
            y_pos = max(0, (canvas_height - scaled_h) // 2)
            
            self.canvas.config(scrollregion=(x_pos, y_pos, x_pos + scaled_w, y_pos + scaled_h))
        else:
            self.canvas.config(scrollregion=self.canvas.bbox("all"))