import cv2
import numpy as np
import matplotlib.pyplot as plt
inpath = "/home/alex/Documents/Clase/2018-2019/VA/Proxecto/project-images/"
outpath = "/home/alex/Documents/Clase/2018-2019/VA/Proxecto/project-results/"

for i in range(1, 13):
    print(i)
    img =cv2.imread(inpath + "im{}.jpeg".format(i), 0)

    #Suavizamos a imaxe para eliminar ruido, escollese este por optimo nos bordes
    #blur = cv2.bilateralFilter(equ,30,75,75)
    blur = cv2.medianBlur(img, 5)

    blur = cv2.bilateralFilter(blur, 15, 30, 30)

    equ = cv2.equalizeHist(blur)
    int, binary = cv2.threshold(equ, 220, 255, cv2.THRESH_BINARY)


    #closingKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35,4))
    #closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE,closingKernel )



    kernel = np.array([[0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255, 0]], np.uint8)
    erode = cv2.erode(binary, kernel)

    closingKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,4))
    closing = cv2.morphologyEx(erode, cv2.MORPH_CLOSE,closingKernel )

    openKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30,15))
    opening = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)

    closingKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,30))
    closing2 = cv2.morphologyEx(erode, cv2.MORPH_CLOSE,closingKernel2 )

    im2, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ###################################
    binaryAux = np.copy(binary)
    cv2.drawContours(binaryAux, contours,  - 1, (0, 0, 0), 3)
    contourLens = contours[len(contours) - 2]

    boundRect = []

    bordes = binary - binaryAux





    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    erode = cv2.erode(bordes, kernel)
    j = 0
    for j in range(len(contours)):
        boundRect.append(cv2.boundingRect(contours[j]))
        x, y, w, h = cv2.boundingRect(contours[j])
        if (w - x) < 500:
            cv2.rectangle(erode,(x, y), (x + w, y + h), (0, 0, 0), -1)
        else:
            cv2.rectangle(erode, (x, y), (x + w, y + h), (255, 255, 255), 2)

    ###################################


    #Ensina as duas imaxes unha aocaron doutra
    backtorgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    two_images = np.concatenate((bordes, erode), axis=1)
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

    #Mide as distancias entre a lente e a cornea
    
        contourLens = np.squeeze(contourLens)
    xvalues_lens = [i[0] for i in contourLens]
    yvalues_lens = [i[1] for i in contourLens]
    contourCornea = contours[len(contours) - 8]
    contourCornea = np.squeeze(contourCornea)
    xvalues_cornea = [i[0] for i in contourCornea]
    yvalues_cornea = [i[1] for i in contourCornea]
    
    distance = []
    j=0
    for j in range(len(xvalues_cornea)):
        for k in range(len(xvalues_lens)):
            if xvalues_cornea[j] == xvalues_lens[k]:
                distance.append(yvalues_cornea[j] - yvalues_lens[k])
    #Ensina as duas imaxes unha aocaron doutra
    two_images = np.concatenate((img, opening), axis=1)
    plt.imshow(two_images)
    plt.xticks([])
    plt.yticks([])
    plt.show()
    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)
    """