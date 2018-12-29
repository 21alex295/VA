import cv2
import numpy as np
import matplotlib.pyplot as plt
impath = "C:/Users/21ale/Pictures/6. AS-OCT/"
img =cv2.imread(impath + "im4.jpeg")

#Suavizamos a imaxe para eliminar ruido
blur = cv2.bilateralFilter(img,15,75,75)
ddd
#erosion para eliminar o que non sexan raias horizontais brancas
kernelErosion = np.ones((1,15),np.uint8)
erosion = cv2.erode(blur,kernelErosion,iterations = 1)


#Dilatacion para esaxerar as liñas brancas sen deformalas ao alto
kernelDilation = np.ones((1,20), np.uint8)
dilation = cv2.dilate(erosion, kernelDilation, iterations=1)


#Pasamos a imaxe a binaria para medir efectivamente as distancias
thresh = 49
im_bw = cv2.threshold(dilation, thresh, 255, cv2.THRESH_BINARY)[1]


#Facemos un closing para pechar os ocos negros da cornea
kernelClosing = np.ones((15,15), np.uint8)
closing = cv2.morphologyEx(im_bw, cv2.MORPH_CLOSE, kernelClosing)

#Opening para eliminar raias da parte de abaixo
kernelOpening = np.ones((3,1), np.uint8)
opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernelOpening)


#Ensina as duas imaxes unha aocaron doutra
two_images = np.concatenate((img, opening), axis=1)
plt.imshow(two_images)
plt.xticks([])
plt.yticks([])
plt.show()