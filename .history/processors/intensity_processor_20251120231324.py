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
        """Display histogram showing pixel value distribution."""
        result = None
        dialog = tk.Toplevel()
        dialog.title("Histogram Viewer")
        dialog.geometry("900x700")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Main frame
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Histogram Viewer", font=("Arial", 14, "bold")).pack(pady=5)

        # Image and histogram preview frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Left: Image preview
        img_frame = ttk.LabelFrame(content_frame, text="Image")
        img_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        h, w = image.shape[:2]
        scale = min(400 / w, 250 / h)
        preview_w, preview_h = int(w * scale), int(h * scale)

        img_canvas = tk.Canvas(img_frame, width=preview_w, height=preview_h, bg="lightgray")
        img_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right: Histogram
        hist_frame = ttk.LabelFrame(content_frame, text="Histogram")
        hist_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        hist_canvas = tk.Canvas(hist_frame, width=450, height=300, bg="white")
        hist_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)

        # Info frame
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)

        info_text = tk.Text(info_frame, height=8, width=80, wrap=tk.WORD, font=("Consolas", 10))
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Calculate and display histogram
        def calculate_histogram():
            try:
                # Display image
                if len(image.shape) == 2:  # Grayscale
                    display_img = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                else:
                    display_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                resized = cv2.resize(display_img, (preview_w, preview_h))
                pil_img = self.Image.fromarray(resized)
                photo = self.ImageTk.PhotoImage(pil_img)
                img_canvas.create_image(preview_w // 2, preview_h // 2, image=photo)
                img_canvas.image = photo

                # Calculate histogram
                hist_canvas.delete("all")
                
                if len(image.shape) == 2:  # Grayscale
                    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
                    
                    # Normalize histogram for display
                    max_val = np.max(hist)
                    hist_normalized = (hist / max_val * 280).astype(int)
                    
                    # Draw histogram
                    for i in range(256):
                        x = 10 + i * 1.7
                        y = 290
                        height = hist_normalized[i][0]
                        hist_canvas.create_line(x, y, x, y - height, fill="gray", width=2)
                    
                    # Statistics
                    mean_val = np.mean(image)
                    std_val = np.std(image)
                    min_val = np.min(image)
                    max_val = np.max(image)
                    
                    info = f"""Image Statistics (Grayscale):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mean:             {mean_val:.2f}
Standard Dev:     {std_val:.2f}
Min Value:        {min_val}
Max Value:        {max_val}
Dimensions:       {w} x {h}
Total Pixels:     {w * h}
"""
                    
                else:  # Color image (BGR)
                    colors = [('blue', 'Blue'), ('green', 'Green'), ('red', 'Red')]
                    color_codes = ['#0000FF', '#00FF00', '#FF0000']
                    
                    stats_info = []
                    
                    for idx, (channel_name, display_name) in enumerate(colors):
                        hist = cv2.calcHist([image], [idx], None, [256], [0, 256])
                        max_val = np.max(hist)
                        hist_normalized = (hist / max_val * 280).astype(int)
                        
                        # Draw histogram
                        for i in range(256):
                            x = 10 + i * 1.7
                            y = 290
                            height = hist_normalized[i][0]
                            hist_canvas.create_line(x, y, x, y - height, fill=color_codes[idx], width=1)
                        
                        # Calculate statistics for this channel
                        channel_data = image[:, :, idx]
                        mean_val = np.mean(channel_data)
                        std_val = np.std(channel_data)
                        stats_info.append(f"{display_name:6s}: Mean={mean_val:6.2f}  Std={std_val:6.2f}")
                    
                    info = f"""Image Statistics (Color - BGR):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{stats_info[0]}
{stats_info[1]}
{stats_info[2]}

Dimensions:       {w} x {h}
Total Pixels:     {w * h}
Channels:         3 (BGR)
"""
                
                # Draw axes
                hist_canvas.create_line(10, 290, 450, 290, fill="black", width=2)  # X-axis
                hist_canvas.create_line(10, 10, 10, 290, fill="black", width=2)    # Y-axis
                
                # Labels
                hist_canvas.create_text(230, 305, text="Pixel Value (0-255)", font=("Arial", 10))
                hist_canvas.create_text(5, 150, text="Frequency", font=("Arial", 10), angle=90)
                
                # Tick marks
                for i in range(0, 256, 64):
                    x = 10 + i * 1.7
                    hist_canvas.create_line(x, 290, x, 295, fill="black", width=1)
                    hist_canvas.create_text(x, 310, text=str(i), font=("Arial", 8))
                
                info_text.delete("1.0", tk.END)
                info_text.insert("1.0", info)
                
            except Exception as e:
                info_text.delete("1.0", tk.END)
                info_text.insert("1.0", f"Error calculating histogram: {str(e)}")

        calculate_histogram()

        # Buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        def save_histogram():
            """Save histogram as image or return image with histogram overlay"""
            try:
                # Create code for histogram calculation
                if len(image.shape) == 2:
                    code = "# Calculate histogram for grayscale image\n"
                    code += "hist = cv2.calcHist([image], [0], None, [256], [0, 256])\n"
                    code += "# Visualize histogram (requires matplotlib)\n"
                    code += "import matplotlib.pyplot as plt\n"
                    code += "plt.plot(hist)\n"
                    code += "plt.title('Grayscale Histogram')\n"
                    code += "plt.xlabel('Pixel Value')\n"
                    code += "plt.ylabel('Frequency')\n"
                    code += "plt.show()\n"
                else:
                    code = "# Calculate histogram for color image (BGR)\n"
                    code += "colors = ('b', 'g', 'r')\n"
                    code += "for i, color in enumerate(colors):\n"
                    code += "    hist = cv2.calcHist([image], [i], None, [256], [0, 256])\n"
                    code += "    plt.plot(hist, color=color)\n"
                    code += "plt.title('Color Histogram')\n"
                    code += "plt.xlabel('Pixel Value')\n"
                    code += "plt.ylabel('Frequency')\n"
                    code += "plt.legend(['Blue', 'Green', 'Red'])\n"
                    code += "plt.show()\n"
                
                nonlocal result
                result = (image.copy(), code)
                messagebox.showinfo("Success", "Histogram code generated!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

        ttk.Button(buttons_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Generate Code", command=save_histogram).pack(side=tk.RIGHT, padx=5)

        dialog.wait_window()
        return result

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
