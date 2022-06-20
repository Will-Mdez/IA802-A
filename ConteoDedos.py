import cv2
import ContadorManos as sm

detector=sm.detectormanos(Confdeteccion=0.75)

cap=cv2.VideoCapture(0)

while True:
    while True:
        # lectura de la camara
        ret, frame = cap.read()
        if ret is False:
            break

        frame = detector.encontrarmanos(frame)

        cv2.rectangle(frame,(420,225),(570,425),(0,0,0),cv2.FILLED)

        cv2.putText(frame,"# Dedos",(425,420),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),5)

        manosInfo,cuadro= detector.encontrarposicion(frame,dibujar=True)

        if len(manosInfo)!=0:
            dedos=detector.dedoarriba()
            contar=dedos.count(1)
            cv2.putText(frame, str(contar), (445, 375), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 25)

        cv2.inshow('Manos', frame)

        t = cv2.waitKey(1)
        if t == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
