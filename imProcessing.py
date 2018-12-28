import cv2
import matplotlib.pyplot as plt
impath = "C:/Users/21ale/Pictures/6. AS-OCT/"
img =cv2.imread(impath + "im4.jpeg")
plt.imshow(img,"gray")