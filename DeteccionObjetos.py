import cv2

class DetectorFondoHomogeneo():
    def __init__(self):
        pass

    def deteccion_objetos(self,frame):
        # Imagen a escala de Grises
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #crear mascara umbral adaptivo
        mask = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,19,5)

        #Deteccion Contornos
        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APROX_SIMPLE)

        #lista de objetos
        objetos_contornos=[]

        for cnt in contornos:
            #Medicion de area de contorno
            area= cv2.contourArea(cnt)
            # Si es mayor a 2000 se agredga a lista
            if area>2000:
                objetos_contornos.append(cnt)
        

        return objetos_contornos