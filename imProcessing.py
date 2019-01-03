import cv2
import numpy as np
import matplotlib.pyplot as plt
inpath = "/home/alex/Documents/Clase/2018-2019/VA/Proxecto/project-images/"
outpath = "/home/alex/Documents/Clase/2018-2019/VA/Proxecto/project-results/"
for i in range(1, 13):
    print(i)
    img =cv2.imread(inpath + "im{}.jpeg".format(i), 0)
    equ = cv2.equalizeHist(img)



    #Suavizamos a imaxe para eliminar ruido, escollese este por optimo nos bordes
    #blur = cv2.bilateralFilter(equ,30,75,75)
    blur = cv2.medianBlur(equ, 9)

    #kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    #sharp = cv2.filter2D(blur, -1, kernel)

    #Pasamos a imaxe a binaria
    thresh = 210
    im_bw = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)[1]


    #Opening para eliminar os puntos brancos que non se eliminaron no suavizado
    kernelOpening = np.ones((2,10), np.uint8)
    opening = cv2.morphologyEx(im_bw, cv2.MORPH_OPEN, kernelOpening)


    #Opening para eliminar os puntos brancos que non se eliminaron no suavizado
    kernelOpening = np.ones((4,10), np.uint8)
    opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernelOpening)



    #Facemos un closing para reconstruir as raias
    kernelClosing = np.ones((1,60), np.uint8)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelClosing)

    canny = cv2.Canny(closing, 200, 255)
    #Ensina as duas imaxes unha aocaron doutra
    two_images = np.concatenate((blur, canny), axis=1)
    cv2.imwrite(outpath + "imres-{}.jpeg".format(i), two_images)

    #plt.imshow(two_images)
    #plt.xticks([])
    #plt.yticks([])
    #plt.show()

    """
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
    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)
    """