import cv2

image = cv2.imread("/home/thach/Python/Computer_Vision_Tutorial/Image_processing_opencv/geforce-ada-4090-web-og-1200x630.jpg")

cv2.imshow("ok",image)
cv2.waitKey(0)
cv2.destroyWindow()