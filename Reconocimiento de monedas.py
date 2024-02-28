import cv2 # Se hace la importación de las librerías con las cuales vamos a trabajar

import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX# Se utiliza este tipo de fuente para lo que se va a escribir en pantalla

cam = cv2.VideoCapture(0)#aquí hacemos el llamado a la cámara donde si ponemos 0  es una cámara exterior o 1 si es la cámara integrada

if not cam.isOpened():#si la camara no conecta o esta fuera de linea 
    raise IOError("Error en la Camara")#nos envia este error si la camara no esta conectada o no es funcional

#se toma los frame que tiene por segundo y los cuales nos reproduce la cámara
while True:
    ret,frame =cam.read()#se toma los frame que tiene por segundo
    frame =cv2.resize(frame,None,fx=1.5,fy=1.5,interpolation=cv2.INTER_AREA)#aquí se toma un cuadro de los fps y se agrega el círculo para que pueda ser identificada la moneda más adelante
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#Se hace el cambio de espacio de color de BGR a HSV
    objetivosa = np.ones((3,3),np.uint8)#devuelve un array del tamaño y tipo indicados sin inicializar sus valores
    objetivosb = np.ones((3,3),np.uint8)

    verde_claro = np.array([50,1,1])#se identifica el color del fondo en el montaje en este caso es verde inicialmente claro y verde oscuro
    verde_oscuro =np.array([100,254,254])
    fondo = cv2.inRange(hsv,verde_claro,verde_oscuro)# Aquí lo que se hace es que se le da un rango a los colores que se escogieron previamente
    circle = cv2.bitwise_not(fondo)#en el operador cv2.bitwise_not , lo que hace es cuando una entrada es verdadera o 1, su salida es falso o  0, y viceversa. En OpenCV se realiza el mismo procedimiento, con la diferencia que en vez de 1 se emplea 255,para poder visualizar el resultado o salida en colores blanco y negro
    objetivo = np.ones((3,3),np.uint8)
    circle =cv2.morphologyEx(circle,cv2.MORPH_OPEN,objetivo)#aquí lo que se hace es una transformación morfológica operación abierta, corrosión avanzada y expansión
    circle =cv2.morphologyEx(circle,cv2.MORPH_CLOSE,objetivo)
    contours,_ = cv2.findContours(circle, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)#se crean los contornos los cuales van a ayudar para la identificación de las monedas y ayuda a detectar formas. (cv2.retr_list) Recupera todos los contornos sin establecer jerarquía (cv2.chain_approx_simple) Comprime segmentos horizontales, verticales y diagonales y deja solo sus puntos finales, ahorrando memoria al no almacenar puntos redundantes
    cv2.drawContours(frame, contours,-1,(0,255,0),2)#se utiliza para crear o dibujar los contornos en la imagen que se obtiene mediante la cámara

#Se le da los valores iniciales a las monedas para que de esta manera nos facilite la suma más adelante de las monedas.
    cincuenta=0
    cien=0
    doscientos=0
    quinientos=0
    mil=0

#se crea este for y lo que hace es, decirnos que el contador es igual al contorno en uno y es la cuenta de los elementos que anteriormente ahí, después se hace el conteo del área
    
    for i in range(len (contours)):
        conteo=contours[i]  
        area = cv2.contourArea(conteo)
        print("area de la moneda",area)

#se le da una condición a cada una de las monedas para de esta manera hacerla únicas y dándole su respectivo valor

        if(10000<area<16500):#condicion de la moneda
            cincuenta=50+cincuenta 
        if(17000<=area<20500):#condicion de la moneda
            cien=100+cien
        if(21000<=area<25500):#condicion de la moneda
            doscientos=200+doscientos
        if(26000<=area<29500):#condicion de la moneda
            quinientos=500+quinientos
        if(29600<=area<36000):#condicion de la moneda
            mil=1000+mil

    total=cincuenta+cien+doscientos+quinientos+mil#se hace la suma de todas las monedas para que nos de el total
    print("Total",total)#se concatena con el total para que de esta manera pueda imprimir el valor
    cv2.putText(frame,"Total: "+str(total),(50,50),font,1,(255,250,100),1)# se pone el texto en una imagen con el color, el tamaño de la fuente  se pone el punto que es de color azul y este por medio de un string se contatena con el numero total, y el texto aparece en las coordenadas 50,50 apartir de la esquina superior izq se le da el tamaño 1 y color azul 

    for i in contours:#se crean los contadores
        fps = cv2.moments(i)# devuelve todos los momentos de la imagen
        cx = int(fps['m10']/fps['m00'])#aqui definimos las coordenadas en x
        cy = int(fps['m10']/fps['m00'])# se definen las coordenadas en y
        cv2.circle(frame,(cx,cy),3,(0,0,255),-1)#define y marca el centro

    cv2.imshow('Contador de Monedas',frame)#nombre de la ventana y muestra la imagen

    c = cv2.waitKey(1)#se crea un break para romper la centencia
    if c == 27:
        break
cam.release()
cv2.destroyAllWindows()#actualiza y refresca todo
    

    
        
