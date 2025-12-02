# Image Processing Studio

A comprehensive, user-friendly GUI application for image processing using OpenCV and Python. This tool allows users to apply a wide range of image transformations, filters, and analysis techniques while viewing the underlying OpenCV code in real-time.

## Features

- **Interactive GUI**: Intuitive interface with real-time image preview.
- **Real-time Code Generation**: Learn OpenCV by seeing the code for every operation you perform.
- **Undo/Redo History**: Experiment freely with full history support.
- **Zoom & Pan**: Inspect images in detail.
- **Extensive Toolset**:
  - **Color Conversions**: Grayscale, HSV, Negative.
  - **Geometric Transformations**: Resize, Rotate, Flip, Perspective, Translation.
  - **Intensity Transformations**: Log, Gamma Correction, Contrast/Brightness.
  - **Morphological Operations**: Erosion, Dilation, Opening, Closing.
  - **Filters & Enhancement**: Gaussian/Median Blur, Histogram Equalization, Contrast Enhancement.
  - **Segmentation & Edge Detection**: Global/Adaptive Thresholding, Canny Edge Detection.
  - **Advanced Processing**: Image Registration (Feature Matching), Image Stitching (Panorama).
  - **Drawing Tools**: Lines, Rectangles, Circles, Text.

## Getting Started

### Prerequisites

- Python 3.x
- OpenCV (`opencv-python`)
- Pillow (`Pillow`)
- Tkinter (usually included with Python)
- NumPy (`numpy`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nvthach124/Visualize_image_processing_app.git
    cd Visualize_image_processing_app
    ```

2.  **Install required packages:**
    ```bash
    pip install opencv-python pillow numpy
    ```
    *(Note: `opencv-contrib-python` might be needed for some advanced features like SIFT if not included in the standard package)*

### Usage

Run the main script to launch the application:

```bash
python main.py
```

## Functionality Overview

### 1. Color Space Conversions
- **Grayscale**: Converts image to black and white.
- **HSV**: Converts to Hue-Saturation-Value color space.
- **Negative**: Inverts pixel values.

### 2. Geometric Transformations
- **Resize**: Scale image by percentage or dimensions.
- **Flip**: Mirror image horizontally, vertically, or both.
- **Rotate**: Rotate by 90-degree increments or arbitrary angles.
- **Move (Translation)**: Shift image along X and Y axes.
- **Perspective Transform**: Correct perspective distortion by selecting 4 points.

### 3. Intensity Transformations
- **Log Transform**: Expands dark values (good for low-contrast images).
- **Power Transform (Gamma)**: Corrects brightness (`gamma < 1` brightens, `gamma > 1` darkens).
- **Contrast & Brightness**: Linear adjustment (`alpha * image + beta`).
- **Histogram Viewer**: View RGB and Grayscale histograms.

### 4. Morphological Operations
- **Erosion**: Erodes away boundaries of foreground objects.
- **Dilation**: Increases the object area.
- **Opening**: Erosion followed by Dilation (removes noise).
- **Closing**: Dilation followed by Erosion (closes small holes).

### 5. Filters & Enhancement
- **Gaussian Blur**: Smooths image using a Gaussian kernel.
- **Median Blur**: Effective for removing salt-and-pepper noise.
- **Histogram Equalization**: Improves contrast by stretching the intensity range.

### 6. Segmentation & Edge Detection
- **Global Thresholding**: Binary thresholding with manual or Otsu's method.
- **Adaptive Thresholding**: Threshold value calculated for smaller regions (Mean or Gaussian).
- **Canny Edge Detection**: Detects edges using multi-stage algorithm with hysteresis.

### 7. Advanced Processing
- **Image Registration**: Aligns a "moving" image to a "reference" image using feature matching (ORB or SIFT) and Homography.
- **Image Stitching**: Combines multiple overlapping images into a seamless panorama.

### 8. Drawing Tools
- Draw **Lines**, **Rectangles**, **Circles**, and add **Text** directly onto the image.

## Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + O` | Open Image |
| `Ctrl + S` | Save Image |
| `Ctrl + R` | Reset Image |
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `+` | Zoom In |
| `-` | Zoom Out |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
