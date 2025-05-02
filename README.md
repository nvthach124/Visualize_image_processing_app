## Overview

This application provides a user-friendly interface for applying common image processing operations using OpenCV in Python. The GUI allows users to load images, apply various transformations, and see the corresponding OpenCV code in real-time.

## Features

- **Interactive GUI**: Easy-to-use interface with image preview
- **Real-time Code Display**: See the OpenCV code for each operation
- **Undo/Redo Functionality**: Track your image processing history
- **Multiple Processing Categories**:
  - Color Space Conversions
  - Transformations
  - Filters & Effects
  - Drawing Operations

## Getting Started

### Prerequisites

- Python 3.x
- OpenCV
- Pillow (PIL)
- Tkinter (usually comes with Python)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nvthach124/Visualize_image_processing_app.git
   cd Visualize_image_processing_app
   ```

2. Install required packages:
   ```bash
   pip install opencv-python pillow
   ```

### Usage

Run the main script to start the application:

```bash
python main.py
```

## OpenCV Image Processing Functions

### 1. Image Input/Output

#### Reading and Displaying Images

```python
image = cv2.imread(file_image_path)
cv2.imshow("window_name", image)  # Displays the image in a window
```

#### Saving Images

```python
cv2.imwrite("new_file_name.jpg", image)
```

### 2. Color Space Conversion

```python
# Convert BGR to Grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Convert BGR to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Convert BGR to RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

### 3. Basic Image Processing

#### Resize Image

```python
resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
```

Parameters:
- `width`, `height`: Target dimensions
- `interpolation`: Method used (options include `cv2.INTER_LINEAR`, `cv2.INTER_CUBIC`, `cv2.INTER_AREA`)

#### Flip Image

```python
flipped_image = cv2.flip(image, flipCode)
```

Parameters:
- `flipCode = 0`: Flip vertically
- `flipCode > 0`: Flip horizontally
- `flipCode < 0`: Flip both horizontally and vertically

#### Rotate Image

```python
# 90° rotation
rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
```

Rotation values:
- `cv2.ROTATE_90_CLOCKWISE`
- `cv2.ROTATE_90_COUNTERCLOCKWISE`
- `cv2.ROTATE_180`

#### Thresholding

```python
_, binary_image = cv2.threshold(gray_image, threshold_value, max_value, threshold_type)
```

Parameters:
- `threshold_value`: Threshold level (0-255)
- `max_value`: Maximum value assigned to pixels above threshold
- `threshold_type`: Type of thresholding (e.g., `cv2.THRESH_BINARY`, `cv2.THRESH_BINARY_INV`)

### 4. Transformations

#### Translation (Moving Image)

```python
# Create translation matrix
M = np.float32([[1, 0, tx], [0, 1, ty]])
# Apply transformation
translated_image = cv2.warpAffine(image, M, (width, height))
```

Parameters:
- `tx`: Horizontal shift
- `ty`: Vertical shift

#### Rotation

```python
# Create rotation matrix
M = cv2.getRotationMatrix2D(center, angle, scale)
# Apply transformation
rotated_image = cv2.warpAffine(image, M, (width, height))
```

Parameters:
- `center`: Point of rotation `(cx, cy)`
- `angle`: Rotation angle in degrees (positive = counterclockwise)
- `scale`: Scaling factor

#### Perspective Transformation

```python
# Create perspective transformation matrix
M = cv2.getPerspectiveTransform(src_points, dst_points)
# Apply transformation
warped_image = cv2.warpPerspective(image, M, (width, height))
```

Parameters:
- `src_points`: Four source points in the original image
- `dst_points`: Four corresponding destination points

### 5. Edge Detection

```python
edges = cv2.Canny(image, threshold1, threshold2)
```

Parameters:
- `threshold1`: Lower threshold for edge detection
- `threshold2`: Upper threshold for edge detection

### 6. Filtering and Smoothing

#### Gaussian Blur

```python
blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
```

Parameters:
- `kernel_size`: Size of kernel (must be odd, e.g., 3, 5, 7)
- `sigma`: Standard deviation (0 = auto-calculated)

#### Median Blur

```python
median_filtered = cv2.medianBlur(image, kernel_size)
```

Parameters:
- `kernel_size`: Size of kernel (must be odd)

### 7. Drawing Functions

#### Line

```python
image = cv2.line(image, (x1, y1), (x2, y2), color, thickness)
```

#### Rectangle

```python
image = cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
```

#### Circle

```python
image = cv2.circle(image, (center_x, center_y), radius, color, thickness)
```

#### Text

```python
image = cv2.putText(image, text, (x, y), font, font_scale, color, thickness, line_type)
```

Parameters:
- `text`: String to display
- `font`: Font type (e.g., `cv2.FONT_HERSHEY_SIMPLEX`)
- `font_scale`: Font size
- `color`: (B, G, R) color tuple
- `thickness`: Line thickness
- `line_type`: Line type (default: `cv2.LINE_AA` for anti-aliased)

## Application Keyboard Shortcuts

- `Ctrl+O`: Open image
- `Ctrl+S`: Save image
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo
- `Ctrl+R`: Reset image
- `+`: Zoom in
- `-`: Zoom out

## Contributing

Contributions to improve the application are welcome! Feel free to submit issues or pull requests.


