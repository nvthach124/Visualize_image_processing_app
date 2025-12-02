import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading

class DefectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phát Hiện Lỗi Ảnh - Image Defect Detection")
        self.root.geometry("1200x800")
        
        # Variables
        self.template_path = None
        self.test_path = None
        self.template_color = None
        self.test_color = None
        self.result_image = None
        self.defect_count = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="HỆ THỐNG PHÁT HIỆN LỖI TRÊN ẢNH", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Điều Khiển", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Template image selection
        ttk.Label(control_frame, text="Ảnh Mẫu (Template):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.template_label = ttk.Label(control_frame, text="Chưa chọn", foreground="gray")
        self.template_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(control_frame, text="Chọn Ảnh Mẫu", 
                  command=self.select_template).grid(row=0, column=2, padx=5)
        
        # Test image selection
        ttk.Label(control_frame, text="Ảnh Kiểm Tra (Test):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.test_label = ttk.Label(control_frame, text="Chưa chọn", foreground="gray")
        self.test_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(control_frame, text="Chọn Ảnh Test", 
                  command=self.select_test).grid(row=1, column=2, padx=5)
        
        # Process button
        self.process_btn = ttk.Button(control_frame, text="Bắt Đầu Phân Tích", 
                                     command=self.process_images, state=tk.DISABLED)
        self.process_btn.grid(row=2, column=0, columnspan=3, pady=15)
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Sẵn sàng", 
                                     font=('Arial', 10))
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Result info
        result_info_frame = ttk.LabelFrame(control_frame, text="Kết Quả", padding="10")
        result_info_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(result_info_frame, text="Số lỗi phát hiện:").grid(row=0, column=0, sticky=tk.W)
        self.defect_count_label = ttk.Label(result_info_frame, text="0", 
                                           font=('Arial', 12, 'bold'), foreground="red")
        self.defect_count_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Save button
        self.save_btn = ttk.Button(control_frame, text="Lưu Kết Quả", 
                                   command=self.save_result, state=tk.DISABLED)
        self.save_btn.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Image display area
        display_frame = ttk.LabelFrame(main_frame, text="Kết Quả Hiển Thị", padding="10")
        display_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Canvas for image display
        self.canvas = tk.Canvas(display_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = ttk.Scrollbar(display_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
    def select_template(self):
        path = filedialog.askopenfilename(
            title="Chọn Ảnh Mẫu",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if path:
            self.template_path = path
            self.template_label.config(text=path.split('/')[-1], foreground="black")
            self.check_ready()
            
    def select_test(self):
        path = filedialog.askopenfilename(
            title="Chọn Ảnh Kiểm Tra",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if path:
            self.test_path = path
            self.test_label.config(text=path.split('/')[-1], foreground="black")
            self.check_ready()
            
    def check_ready(self):
        if self.template_path and self.test_path:
            self.process_btn.config(state=tk.NORMAL)
            
    def process_images(self):
        self.process_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Đang xử lý...")
        
        # Run processing in separate thread
        thread = threading.Thread(target=self.run_detection)
        thread.start()
        
    def run_detection(self):
        try:
            # Load images
            self.template_color = cv2.imread(self.template_path)
            self.test_color = cv2.imread(self.test_path)
            
            if self.template_color is None or self.test_color is None:
                raise Exception("Không thể đọc ảnh. Vui lòng kiểm tra đường dẫn.")
            
            template_gray = cv2.cvtColor(self.template_color, cv2.COLOR_BGR2GRAY)
            test_gray = cv2.cvtColor(self.test_color, cv2.COLOR_BGR2GRAY)
            
            # ORB Feature Matching
            orb = cv2.ORB_create(nfeatures=1000)
            kp1, des1 = orb.detectAndCompute(template_gray, None)
            kp2, des2 = orb.detectAndCompute(test_gray, None)
            
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = sorted(bf.match(des1, des2), key=lambda x: x.distance)
            
            # Homography + Warp
            if len(matches) < 10:
                raise Exception("Không đủ điểm khớp để căn chỉnh ảnh")
                
            src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
            
            h, w = template_gray.shape
            aligned_color = cv2.warpPerspective(self.test_color, M, (w, h))
            aligned_gray = cv2.cvtColor(aligned_color, cv2.COLOR_BGR2GRAY)
            
            # Binary + XOR
            th1 = cv2.adaptiveThreshold(template_gray, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
            th2 = cv2.adaptiveThreshold(aligned_gray, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
            xor_result = cv2.bitwise_xor(th1, th2)
            
            # Morphology Cleaning
            step1 = cv2.medianBlur(xor_result, 5)
            kernel15 = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
            step2 = cv2.morphologyEx(step1, cv2.MORPH_CLOSE, kernel15)
            kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            step3 = cv2.morphologyEx(step2, cv2.MORPH_OPEN, kernel3)
            step4 = cv2.medianBlur(step3, 5)
            kernel29 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (29, 29))
            step5 = cv2.morphologyEx(step4, cv2.MORPH_CLOSE, kernel29)
            step6 = cv2.morphologyEx(step5, cv2.MORPH_OPEN, kernel3)
            final_mask = step6
            
            # Find Defect Contours
            contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            aligned_with_boxes = aligned_color.copy()
            defect_count = 0
            
            for c in contours:
                x, y, w_box, h_box = cv2.boundingRect(c)
                if w_box < 15 or h_box < 15:
                    continue
                defect_count += 1
                cv2.rectangle(aligned_with_boxes, (x, y), (x+w_box, y+h_box), (0, 255, 0), 2)
                cv2.putText(aligned_with_boxes, f"#{defect_count}", (x, y-5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            self.result_image = aligned_with_boxes
            self.defect_count = defect_count
            
            # Update UI in main thread
            self.root.after(0, self.display_result)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))
            
    def display_result(self):
        self.progress.stop()
        self.status_label.config(text="Hoàn thành!")
        self.process_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.defect_count_label.config(text=str(self.defect_count))
        
        # Convert and display image
        if self.result_image is not None:
            img_rgb = cv2.cvtColor(self.result_image, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            
            # Resize if too large
            max_width = 800
            if img_pil.width > max_width:
                ratio = max_width / img_pil.width
                new_size = (max_width, int(img_pil.height * ratio))
                img_pil = img_pil.resize(new_size, Image.Resampling.LANCZOS)
            
            img_tk = ImageTk.PhotoImage(img_pil)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
    def save_result(self):
        if self.result_image is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            cv2.imwrite(file_path, self.result_image)
            messagebox.showinfo("Thành công", f"Đã lưu kết quả tại:\n{file_path}")
            
    def show_error(self, message):
        self.progress.stop()
        self.status_label.config(text="Lỗi xảy ra!")
        self.process_btn.config(state=tk.NORMAL)
        messagebox.showerror("Lỗi", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = DefectDetectionApp(root)
    root.mainloop()