import cv2
from tkinter import *
import sounddevice as sd
import soundfile as sf
import threading as th
import time

def jugar():
    global cap,mov,contador,rostro,jugadores

    contador=0

    jugadores = entrada.get()
    jugadores = int(jugadores)

    #Deteccion de rostro
    rostro = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    #Captura de Video
    cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    #Llamamaos el metodo de deteccion de movimiento
    mov=cv2.createBackgroundSubtractorKNN(history=50,dist2Threshold=2500,detectShadows=False)

    #Deshabilitar OpenCL
    cv2.ocl.setUseOpenCL(False)

    #Funcion Audio

    def audio(archivo):
        global hilo,inicio
        inicio=time.time()
        #Leer Audio
        data,fs=sf.read(archivo)
        #Reproducior Audio
        sd.play(data,fs)

    def check2(hilo):
        fin= time.time()
        tiempo=int(fin-inicio)
        if tiempo > 6:
            Verde()

    def check(hilo):
        fin= time.time()
        tiempo=int(fin-inicio)
        if tiempo>6:
            Roja()

    def Roja():
        
        global jugadores,contador,dis

        dis = 0

        archivo='Roja.mp3'
        hilo= th.Thread(target=audio,args=(archivo,))
        hilo.start()

        while True:
            check2(hilo)
            
            #Lectura de Video
            ret,frame = cap.read()

            #Aplicar filtro Gaussiano
            filtro=cv2.GaussianBlur(frame,(31,31),0)

            #Aplicacion de metodo de deteccion de movimento
            mascara=mov.apply(filtro)

            #Crear copia
            copy= mascara.copy()

            #Buscar los contornos
            contornos,jerarquia=cv2.findContours(copy,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            #mostrar jugadores vivos
            cv2.putText(frame,f"Jugadores Vivos:{str(jugadores)}",(400,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

            #Dibujar Contornos
            for con in contornos:
                #Borramos los contornos peque;os
                if cv2.contourArea(con)<5000:
                    continue
                
                #Obtenermos las coord de contornos
                (x,y,an,al)= cv2.boundingRect(con)

                #Dubujar rectangulo
                #cv2.rectangle(frame,(x,y),(x+an,y+al),(0,0,255),2)

                #Detecccion Rostro
                copia=frame.copy()
                gris = cv2.cvtColor(copia,cv2.COLOR_BGR2GRAY)
                caras=rostro.detectMultiScale(gris,1.3,5)

                #Detecto el rostro del jugador que perdio
                for (x2,y2,an, al) in caras:
                    cv2.rectangle(frame,(x2,y2),(x2+an,y2+al),(0,0,255),2)
                    cv2.putText(frame,f"Jugador {str(contador)} ELIMINADO",(x2 -70,y2-70),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

                    #muerte
                    muerte = len(caras)

                    if dis == 0:
                        contador = contador + muerte
                        
                        jugadores = jugadores - muerte

                        dis = 1
                        
                        if jugadores == 0:
                            cerrar()

                cv2.imshow("LUZ VERDE LUZ ROJA",frame)
                t= cv2.waitKey(27)
                if t== 27:
                    cerrar()


                
    def Verde():
        archivo='Verde.mp3'
        hilo=th.Thread(target=audio,args=(archivo,))
        hilo.start()

        while True:
            check(hilo)
            #Lectura de Video
            ret,frame = cap.read()

            #Aplicar filtro Gaussiano
            filtro=cv2.GaussianBlur(frame,(31,31),0)

            #Aplicacion de metodo de deteccion de movimento
            mascara=mov.apply(filtro)

            #Crear copia
            copy= mascara.copy()

            #Buscar los contornos
            contornos,jerarquia=cv2.findContours(copy,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            #mostrar jugadores vivos
            cv2.putText(frame,f"Jugadores Vivos:{str(jugadores)}",(400,50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)

            #Dibujamos los contornos
            for con in contornos:
                #Borramos los contornos peque;os
                if cv2.contourArea(con)<5000:
                    continue
                
                #Obtenermos las coord de contornos
                (x,y,an,al)= cv2.boundingRect(con)

                #Dubujar rectangulo
                cv2.rectangle(frame,(x,y),(x+an,y+al),(0,0,255),2)

            #Mostramos los frames
            cv2.imshow("LUZ VERDE LUZ ROJA", frame)
            t= cv2.waitKey(27)
            if t== 27:
                cerrar()
            
    Verde()
    
def cerrar():
    #Cerrar Ventanas

    cv2.destroyAllWindows()
    cap.release()
    global pantalla2
    pantalla2= Toplevel()
    pantalla2.title("SQUID GAME")
    pantalla2.geometry("1280x720")
    imagen2=PhotoImage(file="Fin.png")

    plantilla2.Canvas(pantalla2,width=1280,height=720)

    fondo=Label(pantalla2,image=imagen2)
    fondo.place(x=0,y=0,relwidth=1,relheight=1)

    plantilla2.pack()
    pantalla2.mainloop()





def pantalla_principal():

    global pantalla, entrada
    pantalla = Tk()
    pantalla.title("SQUID GAME")
    pantalla.geometry("1280x720")
    imagen = PhotoImage(file="Fondo.jpg")

    #Creacion de pantalla

    plantilla1= Canvas(pantalla,width=1280,height=720)
    plantilla1.pack(fill =  "both", expand=True)
    plantilla1.create_image(0,0,image=imagen,anchor="nw")

    #Imagen boton Jugar y Cerrar
    img1= PhotoImage(file="Jugar.png")
    img2=PhotoImage(file="Cerrar.png")

    boton1=Button(pantalla,text="JUGAR" , height="40",width="300",command=jugar,image=img1)
    buton1pla = plantilla1.create_window(310,580,anchor="nw",window=boton1)

    boton2=Button(pantalla,text="CERRAR" , height="40",width="300",command=cerrar,image=img2)
    buton2pla = plantilla1.create_window(705,580,anchor="nw",window=boton2)

    #Entrada de Numero de Jugadores
    jugadores=StringVar()
    entrada=Entry(pantalla,textvariable=jugadores)
    entradapla=plantilla1.create_window(595,650,anchor="nw",window=entrada)

    pantalla.mainloop()

pantalla_principal()

