
# coding: utf-8

# In[ ]:

#Aplicación que detecta n cantidad de movimientos bruscos horizontales y verticales y envía un mensaje de texto al celular que uno desee.
#Desarrollado por Alejandro Cabrera Lagunes para el Diplomado de Desarrollo Móvil y Procesamiento de Datos - LANIA - Xalapa, Veracruz, México
# 28 de Noviembre de 2014
import android
import math
import time
droide = android.Android()
tolerancia=0
numeroSacudidas=0
numeroCel=0
texto=""
segundosEnEjecucion=0
escucharNotificacion = False

def configuracion():
    droide.dialogCreateAlert("Sacude-SMS","App. que permite detectar una cierta cantidad de sacudidas del celular horizontal o vertialmente durante x cantidad de tiempo y que reacciona enviando un mensaje de texto de forma automática a un determinado celular. A continuación se pedirán 6 datos.")
    droide.dialogSetPositiveButtonText("Ok")
    droide.dialogShow()
    respuesta = droide.dialogGetResponse().result
    droide.dialogCreateInput("1/6 - Tolerancia", "No. de tolerancia, mientras más alta, mas precisa pero requiere un movimiento más rápido (Recomendado 4 para arriba)","","number")
    droide.dialogShow()
    global tolerancia
    tolerancia = droide.dialogGetResponse().result['value']
    if tolerancia == "":
        tolerancia = 30
    droide.dialogCreateInput("2/6 - Numero de sacudidas", "No. máximo de sacudidas para enviar el mensaje (Recomendado 5 para arriba)","","number")
    droide.dialogShow()
    global numeroSacudidas
    numeroSacudidas = droide.dialogGetResponse().result['value']
    if numeroSacudidas =="":
        numeroSacudidas = 30
    droide.dialogCreateInput("3/6 - Numero de Celular", "No. de celular al cual enviar el mensaje","","number")
    droide.dialogShow()
    global numeroCel
    numeroCel = droide.dialogGetResponse().result['value']
    if numeroCel == "":
        numeroCel = 0
    droide.dialogCreateInput("4/6 - Texto a mandar", "Texto que se enviará luego de "+str(numeroSacudidas)+" sacudidas" ,"","text")
    droide.dialogShow()
    global texto
    texto = droide.dialogGetResponse().result['value']
    print (texto)
    droide.dialogCreateInput("5/6 - Tiempo de Ejecución", "Tiempo en que se ejecutará el programa en segundo plano (en segundos)" ,"","number")
    droide.dialogShow()
    global segundosEnEjecucion
    segundosEnEjecucion = droide.dialogGetResponse().result['value']
    if segundosEnEjecucion == "":
        segundosEnEjecucion = 0
    droide.dialogCreateInput("6/6 - Escuchar Notificacion", "¿Deseas escuchar una notificación al mandar el mensaje? 1:Si, 0:No (Si no, se notifica con un mensaje breve en pantalla)" ,"","number")
    droide.dialogShow()
    global  escucharNotificacion
    respuesta = droide.dialogGetResponse().result['value']
    if respuesta == "":
        respuesta = False
    if int(respuesta) == 1:
        escucharNotificacion = True
    return

def comienzaEscucha():
    tiempoActualizaciones = 50  #0.05 segundos
    tiempoTranscurrido = 0
    droide.startSensingTimed(2,tiempoActualizaciones)
    noHayDatos = True
    cantidadHorizontal = 0
    cantidadVertical = 0
    x = 0.0
    ultimaX = 0.0
    deltaX = 0.0
    y = 0.0
    ultimaY = 0.0
    deltaY = 0.0
    z = 0.0
    ultimaZ = 0.0
    deltaZ = 0.0
    segundosParaEjecutarse = int(segundosEnEjecucion)*1000
    while tiempoTranscurrido <= segundosParaEjecutarse:
        x = droide.sensorsReadAccelerometer().result[0]
        y = droide.sensorsReadAccelerometer().result[1]
        z = droide.sensorsReadAccelerometer().result[2]
        if noHayDatos or ultimaX == None:
            ultimaX = x
            ultimaY = y
            ultimaZ = z
            noHayDatos = False
        else:
            deltaX = math.fabs( x - ultimaX )
            deltaY = math.fabs( y - ultimaY )
            deltaZ = math.fabs( z - ultimaZ )
            if deltaX < int(tolerancia):
                deltaX = 0.0
            if deltaY < int(tolerancia):
                deltaY = 0.0
            if deltaZ < int(tolerancia):
                deltaZ = 0.0
            if deltaX > deltaY:
                cantidadHorizontal += 1
                cantidadVertical = 0
            elif deltaX < deltaY:
                cantidadVertical += 1
                cantidadHorizontal = 0
            if (cantidadHorizontal == int(numeroSacudidas)):
                    cantidadVertical = 0
                    cantidadHorizontal = 0
                    droide.smsSend(str(numeroCel),texto)
                    if escucharNotificacion:
                        droide.ttsSpeak("Mensaje enviado al "+str(numeroCel))
                    else:
                        droide.makeToast("Mensaje enviado al "+str(numeroCel))
            elif (cantidadVertical == int(numeroSacudidas)):
                    cantidadHorizontal = 0
                    cantidadVertical = 0
                    droide.smsSend(str(numeroCel),texto)
                    if escucharNotificacion:
                        droide.ttsSpeak("Mensaje enviado al "+str(numeroCel))
                    else:
                        droide.makeToast("Mensaje enviado al "+str(numeroCel))
            ultimaX = x
            ultimaY = y
            ultimaZ = z
            print ("DeltaX: " + str(deltaX) + " | DeltaY: " + str(deltaY) + " | DeltaZ: "+ str(deltaZ))
        time.sleep(tiempoActualizaciones/1000.0)
        tiempoTranscurrido += tiempoActualizaciones
    return

configuracion()
comienzaEscucha()
droide.stopSensing()

