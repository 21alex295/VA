import cv2
import numpy as np
import matplotlib.pyplot as plt
inpath = "/home/alex/Documents/Clase/2018-2019/VA/Proxecto/project-images/"
outpath = "/home/alex/Documents/Clase/2018-2019/VA/Proxecto/project-results/"

for i in range(1, 13):
    print(i)
    # Abrimos as imaxes iterativamente
    img =cv2.imread(inpath + "im{}.jpeg".format(i), 0)

    # Elimina ruido aleatorio
    blur = cv2.medianBlur(img, 5)

    # Suavizamos a imaxe para eliminar ruido, escollese este por optimo nos bordes
    blur2 = cv2.bilateralFilter(blur, 15, 30, 30)

    # Ecualizamos o histograma para que o brillo sexa o mesmo en todas as imaxes
    # e aumentar o contraste
    equ = cv2.equalizeHist(blur2)

    # Pasamos a imaxe a binaria cun threshold alto para eliminar o maximo ruido
    int, binary = cv2.threshold(equ, 210, 255, cv2.THRESH_BINARY)

    # Eliminamos os elementos coa forma do kernel para reducir elementos non
    # desexados con moita anchura, pero que non son raias
    kernel = np.array([[0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255, 0]], np.uint8)
    erode = cv2.erode(binary, kernel)

    # Closing para xuntar trozos das curvas afectados pola anterior erosion
    closingKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 2))
    closing = cv2.morphologyEx(erode, cv2.MORPH_CLOSE,closingKernel, iterations=2)

    # Erosion que elimina bordes das figuras, logo restamos e quedamonos so cos
    # bordes dos elementos
    erodeKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    erode3 = cv2.erode(closing, erodeKernel)
    erode3 = closing - erode3

    # Busca contornos na imaxe, e pasamos a RGB a imaxe para pintar sobre ela
    # Chain approx none tarda moito mais que chain approx simple
    im2, contours, hierarchy = cv2.findContours(erode3,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # Pasa a imaxe binaria a RGB para poder pintar sobre ela
    erodeRGB = cv2.cvtColor(erode3, cv2.COLOR_GRAY2RGB)

    # Encadra os contornos atopados. Pinta e garda aqueles que teñan un ratio
    # de aspecto alto (estean moi estirados) e a sua anchura sexa maior que 1000
    # e a sua altura menor que 430
    curves = []
    for item in contours:
        x, y, w, h = cv2.boundingRect(item)
        aspect_ratio = float(w)/h

        if aspect_ratio > 11 and w > 1000 and y < 430:
            curves.append(item)
            cv2.rectangle(erodeRGB, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # Procedemos so nas imaxes nas que se atoparon mais de 1 contorno
    if len(curves) > 1:
        curves = np.array(curves)
        # Pasamos a imaxe a RGB para poder pintar sobre ela
        backtorgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # Pintamos cornea
        cv2.drawContours(backtorgb, curves, 0, (0,255,255), 4)

        # Parte de abaixo da lente
        cv2.drawContours(backtorgb, curves, 1, (255,120,0), 4)

        # Parte de arriba da lente
        cv2.drawContours(backtorgb, curves,2, (0, 255, 120), 4)

        #FIXME: Esto podese facer solo en dous contornos no canto de en todos
        for j in range(len(curves)):
            curves[j] = curves[j].squeeze()
            fixed_curve = np.unique(curves[j], axis=0)
            curves[j] = fixed_curve

        # Colle a cornea e a lente do conxunto de contornos. Sabemos que e esa
        # debido a que o primeiro contorno e o de mais abaixo, e o segundo de
        # mais abaixo sera a parte de abaixo da lente
        cornea = curves[0].transpose()
        lente = curves[1].transpose()

        lente_x = lente[0]
        cornea_x = cornea[0]
        cornea_y = cornea[1]
        lente_y = lente[1]

        distancia = []
        visitados_lente = []
        visitados_cornea = []
        cornea_x_puntos = []
        cornea_y_puntos = []
        lente_x_puntos = []
        lente_y_puntos = []

        # Corrixe o feito de que os contornos sexan "circulares". Quedase so cun
        # valor de y para cada valor de x
        for j in range(len(lente_x)):
            for k in range(len(cornea_x)):
                if lente_x[j] == cornea_x[k]:
                    if lente_x[j] in visitados_lente:
                        continue
                    visitados_lente.append(lente_x[j])
                    if cornea_x[k] in visitados_cornea:
                        continue
                    visitados_cornea.append(cornea_x[k])

                    # Medimos a distancia entre os puntos da cornea e da lente
                    distancia_local = cornea_y[k] - lente_y[j]
                    distancia.append(distancia_local)

                    # Gardamos os puntos de unha soa liña do contorno
                    cornea_x_puntos.append(cornea_x[k])
                    cornea_y_puntos.append(cornea_y[k])
                    lente_x_puntos.append(lente_x[j])
                    lente_y_puntos.append(lente_y[j])

        cornea_x = np.array(cornea_x_puntos)
        cornea_y = np.array(cornea_y_puntos)
        lente_x = np.array(lente_x_puntos)
        lente_y = np.array(lente_y_puntos)

        # Pinta cores sobre a imaxe para ver a distancia visualmente
        # FIXME Podese facer de forma mais eficiente
        if distancia:
            visitados_cornea = []
            visitados_lente = []
            for j in range(len(lente_x)):
                for k in range(len(cornea_x)):
                    if lente_x[j] == cornea_x[k]:
                        if lente_x[j] in visitados_lente:
                            continue
                        visitados_lente.append(lente_x[j])
                        if cornea_x[k] in visitados_cornea:
                            continue
                        visitados_cornea.append(cornea_x[k])
                        distancia_local = cornea_y[k] - lente_y[j]
                        color = (((distancia_local - min(distancia)) * (
                                    255 - 0)) / (
                                         max(distancia) - min(distancia))) + 0
                        cv2.line(backtorgb, (lente_x[j], lente_y[j]), (cornea_x[k], cornea_y[k]), (255 - color,0,color), 1)


        # Plot das medicions da distancia lente-cornea
        plt.clf()
        plt.ioff()
        plt.figure(figsize=(20,5))
        plt.plot(distancia)
        plt.savefig(outpath + "plot-{}.png".format(i))

        # Garda duas imaxes cos resultados parciais ou finais que se escollan
        two_images = np.concatenate((backtorgb, erodeRGB), axis=1)
        cv2.imwrite(outpath + "imres-{}.jpeg".format(i), two_images)