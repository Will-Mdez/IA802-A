import cv2
import numpy as np
from DeteccionObjetos import *

#Cargamos el marcador aruco
#ARUCO = objeto utlizado para la observacion de sistemas de imagenes
#el cual aparece en la imagen para ser usado como punto de referecia o de medida
parametros = cv2.aruco.DetectorParameters_create()
diccionario = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)

#cargar detector de objetos
detector=DetectorFondoHomogeneo()

#Captura de camara

cap= cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    #lectura de la camara
    ret,frame=cap.read() 
    if ret is False:
        break

    #Detectar marcador aruco
    esquinas, _, _=cv2.aruco.detectMarkers(frame,diccionario,parameters = parametros)
    esquinas_ent = np.int0(esquinas)
    cv2.polylines(frame,esquinas_ent,True,(0,0,255),5)

    #Perimetro de Aruco
    perimetro_aruco=cv2.arcLength(esquinas_ent[0], True)
    #print(perimetro)

    #proporcion en CM
    proporcion_cm = perimetro_aruco/16
    #print(proporcion_cm)

    #Deteccion de Objetos
    contornos=detector.deteccion_objetos(frame)

    #Dibujar contorno de objetos
    for cont in contornos:
        #Dibujar contorno de objetos
        #cv2.polylines(frame,[cont],True,(0,255,0),2)

        #Rectangulo del objeto
        #A partir del poligono, obtener el rectangulo
        rectangulo = cv2.minAreaRect(cont)
        (x,y), (an,al),angulo= rectangulo

        #pasamos a cm en ancho y alto
        ancho = an/proporcion_cm
        alto = al/proporcion_cm

        #Dibujamos un circulo en la mitad del rectagulo---Para referenciarlo
        cv2.circle(frame,(int(x),int(y)),5,(255,255,0),-1)

        #Dibujar el rectangulo
        rect = cv2.boxPoints(rectangulo)
        rect = np.int0(rect)

        cv2.polylines(frame,[rect],True,(0,255,0),2)

        #Mostrar la info en pixeles
        cv2.putText(frame,"Ancho: {} cm".format(round(ancho,1)),(int(x),int(y-15)),cv2.LINE_AA,0.8,(150,0,255),2)
        cv2.putText(frame,"Ancho: {} cm".format(round(alto,1)),(int(x),int(y+15)),cv2.LINE_AA,0.8,(75,0,75),2)


    #MOstrar fotogramas
    cv2.inshow('Medicion de Objetos',frame)

    t=cv2.waitKey(1)
    if t == 27:
        break


cap.release()
cv2.destroyAllWindows()

