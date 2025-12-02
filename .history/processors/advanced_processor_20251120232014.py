"""
Advanced Image Processing

Handles image registration and stitching operations.
This imports the original implementations from process_monolithic_backup.py
"""
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from .base_processor import BaseProcessor

class AdvancedProcessor(BaseProcessor):
    """Processor for advanced operations - wraps original implementation."""
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
        dialog.geometry("1000x800")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Main frame
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=f"Image Stitching - {len(images)} images selected", 
                 font=("Arial", 14, "bold")).pack(pady=5)

        # === PREVIEW SELECTED IMAGES ===
        # Scrollable frame for selected images
        images_frame = ttk.LabelFrame(main_frame, text="Selected Images (in order)")
        images_frame.pack(fill=tk.X, padx=5, pady=10)

        # Create canvas with scrollbar for image previews
        canvas_container = ttk.Frame(images_frame)
        canvas_container.pack(fill=tk.X, padx=5, pady=5)

        preview_canvas = tk.Canvas(canvas_container, height=150, bg="lightgray")
        preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=preview_canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        preview_canvas.configure(xscrollcommand=scrollbar.set)

        # Frame inside canvas to hold images
        images_inner_frame = ttk.Frame(preview_canvas)
        preview_canvas.create_window((0, 0), window=images_inner_frame, anchor='nw')

        # Display each image as thumbnail
        thumbnail_size = 120
        image_photos = []  # Keep references to prevent garbage collection
        
        for idx, img in enumerate(images):
            img_frame = ttk.Frame(images_inner_frame, relief=tk.RIDGE, borderwidth=2)
            img_frame.pack(side=tk.LEFT, padx=5, pady=5)

            # Resize image to thumbnail
            h, w = img.shape[:2]
            scale = min(thumbnail_size / w, thumbnail_size / h)
            thumb_w, thumb_h = int(w * scale), int(h * scale)
            
            thumb = cv2.resize(img, (thumb_w, thumb_h))
            if len(thumb.shape) == 2:
                thumb_rgb = cv2.cvtColor(thumb, cv2.COLOR_GRAY2RGB)
            else:
                thumb_rgb = cv2.cvtColor(thumb, cv2.COLOR_BGR2RGB)
            
            pil_thumb = self.Image.fromarray(thumb_rgb)
            photo_thumb = self.ImageTk.PhotoImage(pil_thumb)
            image_photos.append(photo_thumb)

            # Canvas for thumbnail
            thumb_canvas = tk.Canvas(img_frame, width=thumb_w, height=thumb_h, 
                                    bg="white", highlightthickness=0)
            thumb_canvas.pack(padx=2, pady=2)
            thumb_canvas.create_image(thumb_w // 2, thumb_h // 2, image=photo_thumb)

            # Label with image number and size
            if idx == 0:
                label_text = f"Current\n{w}×{h}"
            else:
                label_text = f"Image {idx}\n{w}×{h}"
            
            ttk.Label(img_frame, text=label_text, font=("Arial", 9)).pack()

        # Update scroll region
        images_inner_frame.update_idletasks()
        preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))

        # === STITCHING RESULT PREVIEW ===
        result_frame = ttk.LabelFrame(main_frame, text="Stitching Result")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        # Canvas for result with scrollbars
        canvas_frame = ttk.Frame(result_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        result_canvas = tk.Canvas(canvas_frame, bg="lightgray", height=350)
        result_canvas.grid(row=0, column=0, sticky="nsew")

        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=result_canvas.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=result_canvas.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")

        result_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        # Variables
        mode_var = tk.StringVar(value="panorama")

        # Controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Label(controls_frame, text="Stitch Mode:").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="Panorama", variable=mode_var, value="panorama").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="Scans", variable=mode_var, value="scans").pack(side=tk.LEFT, padx=5)

        info_label = ttk.Label(controls_frame, text="", foreground="blue")
        info_label.pack(side=tk.LEFT, padx=20)

        progress_label = ttk.Label(controls_frame, text="")
        progress_label.pack(side=tk.LEFT, padx=10)

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
                max_display_w, max_display_h = 950, 330
                scale = min(max_display_w / w, max_display_h / h, 1.0)  # Don't upscale
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
