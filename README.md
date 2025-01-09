## Basic Image Processing Functions in Opencv-Python
This repository demonstrates essential image processing techniques using OpenCV in Python. These operations are foundational for many computer vision tasks.

## Introduction

OpenCV (Open Source Computer Vision Library) is a popular library for computer vision and image processing tasks. This repository provides basic examples to get started with image processing, including image transformations, filtering, and edge detection.

## Bacsic Functions
 #### 1) Reading, Display and Writing Images.
  - Load images and show.
    
    ```bash
       image = cv2.imread(file_image_path)
       cv2.imshow("window_name", image) #Displays the image in a window.
    ```
  - Save processed images
     ```bash
      cv2.imwrite("new_file_name",image).
    ```
  #### 2) Color Space Conversion.
  - code: The color space conversion code, specified by constants (like 'cv2.COLOR_BGR2GRAY', 'cv2.COLOR_BGR2HSV', etc).
    ```bash
      image = cv2.cvtColor(image, code).
    ```
  #### 3) Basic image processing.
  - Resize image:
    ```bash
      resized_image = cv2.resize(image, dsize, interpolation)
    ```
      - dsize: Output size (width, height).
      - interpolation: Interpolation method (like cv2.INTER_LINEAR, cv2.INTER_AREA, etc).
  - Flip image:
     ```bash
      flipped_image = cv2.flip(image, flipCode)
    ```
     - flipCode = 0: Flip vertically.
     - flipCode > 0: Flip horizontally.
     - flipCode < 0: Flip both horizontally and vertically.
  - Rotate image:
     ```bash
      rotated_image = cv2.rotate(image,Rotation_values )
    ```
     - Rotation_values:
       - cv2.ROTATE_90_CLOCKWISE: Rotate 90 degrees clockwise.
       - cv2.ROTATE_90_COUNTERCLOCKWISE: Rotate 90 degrees counterclockwise.
       - cv2.ROTATE_180: Rotate 180 degrees.
  - Binary thresholding:
    Apply binarization to convert the image to binary form.
     ```bash
      _, binary_image = cv2.threshold(image, thresh, maxval, type)
    ```
     - Parameters 
       - thresh: Threshold value (0-255).
       - maxval: Maximum value assigned to pixels exceeding the threshold (0-255).
       - type: Threshold type (cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, ...).
#### 4) Transformations.
  - Apply affine transformations (translation, rotation, scaling).
     ```bash
      transformed_image = cv2.warpAffine(image, M, dsize = (width, height))
    ```
     M: The transformation matrix used to apply transformations to the image.
      - Translation Matrix:
        ```bash
           M = np.float32([[1, 0, tx], [0, 1, ty]])
        ```
        - tx​ : Move along the x-axis.
        - ty​ : Move along the y-axis.
      - Rotation Matrix:
        ```bash
            M = cv2.getRotationMatrix2D(center, angle, scale)
        ```
        - center: (cx, cy)  # Center of rotation.
        - angle: Calculated in degrees and Positive for anti-clockwise and negative for clockwise.
        - scale: scaling factor which scales the image
      - Linear Transformation Matrix:
        Apply linear transformations such as Rotation, Scaling, Shearing.
        ```bash
          pts1,2 = np.float32([[a11, a21],
                     [a21, a22], 
                     [b1, b2]])
          M = cv2.getAffineTransform(pts1, pts2)
        ```
        - aij​: Linear transformation coefficient.
        - b1​,b2​: Displacement.
  - Perspective transformation.
     ```bash
      transformed_image = cv2.warpPerspective(image, M, (width, height))
    ```
     - Perspective Transformation Matrix:
        ```bash
           M = cv2.getPerspectiveTransform(src, dst) 
        ```
        - src: Coordinates of quadrangle vertices in the source image.
        - dst: Coordinates of the corresponding quadrangle vertices in the destination image.
 #### 5) Edge and Boundary Detection.
  - Edge detection using Canny algorithm.
      ```bash
        edges = cv2.Canny(image, threshold1, threshold2)
      ```
      - threshold1: Low threshold (0-255).
      - threshold2: High threshold (0-255).
 #### 6) Filter and Smooth Images.
   - Gaussian filter:
      ```bash
        blurred_image = cv2.GaussianBlur(image, (ksize, ksize), sigmaX)
      ```
     - ksize: Kernel size (must be odd, e.g. (3, 3)).
     - sigmaX: Standard deviation along the X axis (can be set to 0 for OpenCV to calculate automatically).
   - Nedian filter:
      ```bash
        median_image = cv2.medianBlur(image, ksize)
      ```
      -ksize: Kernel size (must be odd, e.g. 3, 5, 7, ... )).
 #### 7) Drawing Shapes and Text.
   - Lines:
      ```bash
        image = cv2.line(image, (x1, y1), (x2, y2), color, thickness)
      ```
  - Rectangle:
    ```bash
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
      ```
  - Circle:
    ```bash
        cv2.circle(image, (center_x, center_y), radius, color, thickness)
      ```
  - Text:
    ```bash
        cv2.putText(image, text, (x, y), font, fontScale, color, thickness, lineType)
      ```
  - Parameters:
    - text: Text content.
    - (x, y): Coordinates of the lower left corner of the text.
    - font: Font style (cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_COMPLEX, ...).
    - fontScale: Font size.
    - color: Color.
    - thickness: Thickness.
    - lineType: Line style
## Above is one of the basic image processing functions in opencv, there are also other functions,... Thank you for reading, Let try it!
 
 
