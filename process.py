import cv2
import tkinter as tk
from tkinter import messagebox
import numpy as np


class FunctionsProcessing:
    def cvt_RGB(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "cv2.cvtColor(image, cv2.COLOR_BGR2RGB)\n"

    def cvt_HSV(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV), "cv2.cvtColor(image, cv2.COLOR_BGR2HSV)\n"

    def cvt_GRAY(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), "cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"

    def resize_image(self, image):
        return cv2.resize(image, (200, 200)), "cv2.resize(image, (200, 200))\n"

    def rotate_image(self, image):
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE), "cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)\n"

    def threshold_image(self, image):

        result = None
        new_window = tk.Tk()
        new_window.title("Nhập")

        tk.Label(new_window,font=("Arial", 12), text="Nhập giá trị ngưỡng (0-255):").pack()
        entry1 = tk.Entry(new_window,font=("Arial", 12))
        entry1.pack(pady=10)

        tk.Label(new_window,font=("Arial", 12), text="Nhập giá trị tối đa gán cho pixel vượt ngưỡng (0-255):").pack()
        entry2 = tk.Entry(new_window,font=("Arial", 12))
        entry2.pack(pady=10)

        def get_value():
            nonlocal result
            try:
                thresh = float(entry1.get())
                maxval = float(entry2.get())

                if not (0 <= thresh <= 255) or not (0 <= maxval <= 255):
                    messagebox.showerror("Lỗi", "Giá trị ngưỡng và giá trị tối đa (0-255).")
                    return
                    # Thực hiện threshold và lưu kết quả vào biến result
                ret, thresholded_image = cv2.threshold(image, thresh, maxval, cv2.THRESH_BINARY)
                result = (thresholded_image, f"cv2.threshold(image, {thresh}, {maxval}, cv2.THRESH_BINARY)\n")

                new_window.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

        button = tk.Button(new_window, text="Ok", command=get_value)
        button.pack(pady=10)
        new_window.wait_window()
        return result

    def equalized_image(self, image):
        try:
            return cv2.equalizeHist(image), "cv2.equalizeHist(gray_image)\n"
        except:
            messagebox.showerror("Lỗi", "Request to convert to grayscale first.")

    def move_image(self, image):
        result = None
        new_window = tk.Tk()
        new_window.title("Nhập")

        tk.Label(new_window,font=("Arial", 12), text="Nhập tx:").pack()
        entry1 = tk.Entry(new_window,font=("Arial", 12))
        entry1.pack(pady=10)

        tk.Label(new_window,font=("Arial", 12), text="Nhập ty:").pack()
        entry2 = tk.Entry(new_window,font=("Arial", 12))
        entry2.pack(pady=10)

        def get_value():
            nonlocal result
            try:
                tx = int(entry1.get())
                ty = int(entry2.get())
                h, w = image.shape[:2]
                M = np.array([[1, 0, tx],
                              [0, 1, ty]], dtype=np.float32)
                new_window.destroy()

                result = cv2.warpAffine(image, M, (w, h)), f"M = np.array([[1, 0, {tx}],[0, 1, {ty}]], dtype=np.float32)\ncv2.warpAffine(image, M, (w, h))\n"

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

        button = tk.Button(new_window, text="Ok", command=get_value)
        button.pack(pady=10)
        new_window.wait_window()
        return result

    def rotationMatrix2d(self, image):
        result = None
        new_window = tk.Tk()
        new_window.title("Nhập")

        tk.Label(new_window,font=("Arial", 12), text="Nhập angle (-360-> 360):").pack()
        entry1 = tk.Entry(new_window,font=("Arial", 12))
        entry1.pack(pady=10)

        tk.Label(new_window,font=("Arial", 12), text="Nhập scale:").pack()
        entry2 = tk.Entry(new_window,font=("Arial", 12))
        entry2.pack(pady=10)

        def get_value():
            nonlocal result
            try:
                angle = float(entry1.get())
                scale = float(entry2.get())
                h, w = image.shape[:2]

                new_window.destroy()

                h, w = image.shape[:2]
                M = cv2.getRotationMatrix2D((w // 2, h // 2), angle=angle, scale=scale)

                result = cv2.warpAffine(image, M, (w,h)), f"M = cv2.getRotationMatrix2D((w // 2, h // 2), angle= {angle}, scale = {scale})\ncv2.warpAffine(image, M, (w, h))\n"

            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

        button = tk.Button(new_window, text="Ok", command=get_value)
        button.pack(pady=10)
        new_window.wait_window()
        return result


    def canny_detection(self, image):
        result = None
        new_window = tk.Tk()
        new_window.title("Nhập")

        tk.Label(new_window,font=("Arial", 12), text="Nhập giá trị ngưỡng dưới (low threshold(0-255)):").pack()
        entry1 = tk.Entry(new_window,font=("Arial", 12))
        entry1.pack(pady=10)

        tk.Label(new_window,font=("Arial", 12), text="Nhập giá trị ngưỡng trên (high threshold(0-255)):").pack()
        entry2 = tk.Entry(new_window,font=("Arial", 12))
        entry2.pack(pady=10)

        def get_value():
            nonlocal result
            try:
                thresh1 = float(entry1.get())
                thresh2 = float(entry2.get())

                if not (0 <= thresh1 <= 255) or not (0 <= thresh2 <= 255):
                    messagebox.showerror("Lỗi", "Giá trị ngưỡng và giá trị tối đa (0-255).")
                    return
                    # Thực hiện threshold và lưu kết quả vào biến result

                result = cv2.Canny(image, thresh1, thresh2), f"cv2.Canny(image, {thresh1}, {thresh2})\n"

                new_window.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

        button = tk.Button(new_window, text="Ok", command=get_value)
        button.pack(pady=10)
        new_window.wait_window()
        return result

    def gaussianBlur(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0), "cv2.GaussianBlur(image,(5,5),0)\n"

    def medianBlur(self, image):
        return cv2.medianBlur(image, ksize=5), "cv2.medianBlur(image,ksize = 5)\n"

    def draw_Line(self, image):
        return cv2.line(image, pt1=(50, 50), pt2=(450, 50), color=(255, 0, 0),
                        thickness=2), "cv2.line(image, pt1= (50, 50),pt2= (450, 50),color = (255, 0, 0), thickness = 2)\n"

    def draw_Rectangle(self, image):
        return cv2.rectangle(image, (80, 80), (300, 500), (255, 0, 0),
                             2), "cv2.rectangle(image, (80, 80), (300, 500), (255, 0, 0), 2)\n"

    def draw_Circle(self, image):
        return cv2.circle(image, center=(400, 400), radius=50, color=(255, 0, 0),
                          thickness=2), " cv2.circle(image, center=(400, 400), radius=50, color=(255, 0, 0), thickness=2)\n"

    def put_Text(self, image):
        return cv2.putText(image, "text", (200, 300), cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(255, 0, 0),
                           thickness=2), """cv2.putText(image, "text", (200, 300), cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(255, 0, 0), thickness=2)\n"""
