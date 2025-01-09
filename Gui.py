from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from process import *


class GUI:
    def __init__(self,root):
        self.file_path = None
        self.display_Image = None
        self.canvas = None
        self.scale = None
        self.functions = None
        self.transformation = StringVar(value="Grayscale")
        self.code_display = None
        self.code_text = ""
        self.set_code_text = StringVar(value="")
        self.fp = FunctionsProcessing()
        self.root = root
        self.setUpGUI()
    def setUpGUI(self):
        self.root.title("Image Processing App")
        self.root.geometry("1450x880")

        self.functions = [
            ("BGR to RGB"    , "BGR to RGB"    ),
            ("BGR to Gray"   , "BGR to Gray"   ),
            ("BGR to HSV"    , "BGR to HSV"    ),
            ("Resize"        , "Resize"        ),
            ("Flip"          , "Flip"          ),
            ("Rotate_90"     , "Rotate_90"     ),
            ("Threshold"     , "Threshold"     ),
            ("Equalized"     , "Equalized"     ),
            ("Move"          , "Move"          ),
            ("Rotate Matrix" , "Rotate Matrix" ),
            ("Perspective"   , "Perspective"   ),
            ("Canny"         , "Canny"         ),
            ("GaussianBlur"  , "GaussianBlur"  ),
            ("MedianBlur"    , "MedianBlur"    ),
            ("Draw line"     , "Draw line"     ),
            ("Draw rectangle", "Draw rectangle"),
            ("Draw circle"   , "Draw circle"   ),
            ("Put text"      , "Put text"      ),
        ]

        self.scale = 1.0
        # Load image button
        Button(self.root, font=("Arial", 15), text="Load File", command=self.load_image).place(x=50, y=30)
        Button(self.root, font=("Arial", 15), text="Reload Image", command=self.reload_image).place(x=1245, y=30)
        # Display image
        self.canvas = Canvas(self.root, width=1000, height=550, bg="lightgray")
        self.canvas.place(x=200, y=50)

        for i, (label, transformation) in enumerate(self.functions):
            if i<9:
                Button(self.root, text=label, font=("Arial", 11), height=2, width=10,
                   command=lambda t=transformation: self.apply_transformation(t)).place(x=50,
                                                                                        y=100 + i * 50)
            else:
                Button(self.root, text=label, font=("Arial", 11), height=2, width=10,
                   command=lambda t=transformation: self.apply_transformation(t)).place(x=1240,
                                                                                        y=100 + (i-9) * 50)

        # Zoom buttons
        Button(self.root, text="Zoom +", command=self.zoom_in).place(x=650, y=620)
        Button(self.root, text="Zoom -", command=self.zoom_out).place(x=750, y=620)

        # Code display
        Label(self.root, font=("Arial", 12), text="Code for Transformation:").place(x=600, y=650)
        # Create fonts with different weights and slants
        self.code_display = Text(self.root, font=("Arial", 14), width=80, height=10)
        self.code_display.place(x=200, y=670)

        self.set_code_text.trace("w",
                                 lambda *args: self.code_display.delete("1.0", "end") or self.code_display.insert("1.0",
                                                                                                                  self.set_code_text.get()))

    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        if self.file_path:
            self.display_Image = cv2.imread(self.file_path)
            self.code_text = "cv2.imread(" +"'" + self.file_path+ "'"+ ")\n"
            self.set_code_text.set(self.code_text)
            self.update_image()

    def reload_image(self):
        self.display_Image = cv2.imread(self.file_path)
        self.scale = 1.0
        self.code_text = "cv2.imread(" + self.file_path + ")\n"
        self.set_code_text.set(self.code_text)
        self.update_image()

    def update_image(self):

        # Scale the image
        h, w = self.display_Image.shape[:2]
        resized_image = cv2.resize(self.display_Image, (int(w * self.scale), int(h * self.scale)))

        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image_rgb)
        img_tk = ImageTk.PhotoImage(img)

        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor='nw', image=img_tk)

    def zoom_in(self):

        self.scale *= 1.1
        self.update_image()

    def zoom_out(self):

        self.scale *= 0.9
        self.update_image()

    def apply_transformation(self, transformation):
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
            "GaussianBlur"  : self.fp.gaussianBlur,
            "MedianBlur"    : self.fp.medianBlur,
            "Draw line"     : self.fp.draw_Line,
            "Draw rectangle": self.fp.draw_Rectangle,
            "Draw circle"   : self.fp.draw_Circle,
            "Put text"      : self.fp.put_Text,
        }
        temp_image, code = func_map[transformation](self.display_Image)
        self.code_text += code
        self.display_Image = temp_image
        self.set_code_text.set(self.code_text)
        self.update_image()


