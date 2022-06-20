from http.cookiejar import Cookie
import cv2
import numpy as np
from filtrokalman import FiltroKalman

#Iniciamos el filtro Kalman

fk = FiltroKalman()
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

while(True):
    #Lectura de Video
    ret,frame= cap.read()

    #VEririficacion de video
    if ret is False:
        break

    #Preprocesamiento de zona de interes
    mB = np.matrix(frame[:,:,0])
    mG = np.matrix(frame[:,:,1])
    mR = np.matrix(frame[:,:,2])

    #COlor
    Color = cv2.absdiff(mG,mB)

    #Binarizamos la imagne
    _, umbral = cv2.threshold(Color,50,255,cv2.THRESH_BINARY)

    #extraemos contornos de la zona seleccionada
    contornos, _= cv2.findContours(umbral,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #Ordenamos del mayor a menor
    contornos= sorted(contornos,key=lambda x: cv2.contourArea(x),reverse=True)

    for contorno in contornos:
        
        area= cv2.contourArea(contorno)
        if area > 500:
            #Deteccion de placa    
            x,y,ancho,alto= cv2.boundingRect(contorno)

            #Extraccion de coordenadas
            xi=x    #Coord de la placa en X inicial
            yi=y    #Coord de la placa en Y incial

            xf= x+ancho  # Coord de la placa en xfinal
            yf = y+alto     # COord de la placa en y final

            #dibijamos rectangula
            cv2.rectangle(frame,(xi,yi),(xf,yf),(255,0,0),2)

            #dibujamos el centro
            cx = int((xi+xf)/2)
            cy = int((yi+yf)/2)

            cv2.circle(frame,(cx,cy),10,(0,0,255),-1)

            #Trayectoria

            predict= fk.prediccion(cx,cy)
            predict2 = fk.prediccion(predict[0],predict[1])
            predict3 = fk.prediccion(predict2[0],predict2[1])
            predict4 = fk.prediccion(predict3[0],predict3[1])
            predict5 = fk.prediccion(predict4[0],predict4[1])

            #Dibujo de la trayectoria
            cv2.circle(frame,(predict[0],predict[1]),10,(0,0,255),-1)
            cv2.circle(frame,(predict2[0],predict2[1]),10,(0,0,255),-1)
            cv2.circle(frame,(predict3[0],predict3[1]),10,(0,0,255),-1)
            cv2.circle(frame,(predict4[0],predict4[1]),10,(0,0,255),-1)
            cv2.circle(frame,(predict5[0],predict5[1]),10,(0,0,255),-1)
    

    #Mostramos en video
    cv2.imshow("Prediccion de Traectoria",frame)
    #cv2.imshow("Mascara",umbral)

    #Lectura de teclado
    t=cv2.waitKey(1)
    if t == 27:
        break


cap.release()
cv2.destroyAllWindows()
