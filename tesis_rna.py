#Red neuronal para el reconocimineto de patrones de datos ONI y la irradiancia solar
#
# Autor: Eric Alberto Suárez Gallareta
#

#Librerias
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as tls
import scipy.io
from PyEMD import EMD
import sympy as sy
import tensorflow as tf
import tflearn

#documentos con los datos
#datos ONI
datos_oni = open('Mensuales_ONI.dat')

#datos IST
datos_IST = open('TSI_reconstruc.dat')

#función para generar data frames
#datame para datos eje y
array1year=[]
array1month=[]
array2=[]

for line in datos_oni:
    #array.append(re.findall(pattern,line))
    array1year.append(line[0:4])
    array1month.append(line[4:6])
    
    if line[7]=='-':
        array2.append(line[7:])
        
    else:
        array2.append(line[7:])
  
lista = []
lista2 = []
listaGeneral = []
for valor in array2:
    lista.append(valor.rstrip('\n'))



for sal in range(len(lista)):
    lista2.append(array1year[sal]+array1month[sal])


listaGeneral = dict(zip(lista2[1:], lista[1:]))
tupla = listaGeneral.items()
df = pd.DataFrame(list(tupla))
df.columns = [ "fecha", "valor"]
y = df['valor'].astype(float)
x = df['fecha'].astype(float) 




#DME
def dme_function(lista_para_ejecutar):
    nueva_list = lista_para_ejecutar
    new_data =[]
    for item in nueva_list:
        new_data.append(float(item))
    #x = np.linspace(0, 10, len(lista_para_ejecutar))
    signal = np.array(new_data)
    emd = EMD()
    IMFS = emd.emd(signal)
    return IMFS


#derivadas
def derivar(dme_para_derivar):
    derivada = []
    reversearray = dme_para_derivar[::-1]
    for line in range(len(reversearray)-1):
        operacion = reversearray[line]-reversearray[line+1]
        derivada.append(operacion)
    derivada.append(derivada[0])
    mi_derivada = derivada[::-1]
    return mi_derivada

#creación de la red neuronal artificial
#preparación de los datos para el entrenamiento
trainY = np.float32(y)
trainX = np.float32(x)

trainX = trainX.reshape(89,7)

trainY = trainY.reshape(89,7)

#creacion de las neuronas para cada capa
entradas = 7
capa1 = 128
capa2 = 128
capa3 = 128
capa4 = 128
capa5 = 128
capa6 = 128
capa7 = 128
capa8 = 128
capa9 = 128
capa10 = 128
salida = 7

#creación del modelo de la RNA
def crear_modelo():
    tf.reset_default_graph()
    red = tflearn.input_data([None, entradas])
    red = tflearn.fully_connected(red, capa1, activation='softsign')
    red = tflearn.fully_connected(red, capa2, activation='softsign')
    red = tflearn.fully_connected(red, capa3, activation='softsign')
    red = tflearn.fully_connected(red, capa4, activation='softsign')
    red = tflearn.fully_connected(red, capa5, activation='softsign')
    red = tflearn.fully_connected(red, capa6, activation='softsign')
    red = tflearn.fully_connected(red, capa7, activation='softsign')
    red = tflearn.fully_connected(red, capa8, activation='softsign')
    red = tflearn.fully_connected(red, capa9, activation='softsign')
    red = tflearn.fully_connected(red, capa10, activation='softsign')
    red = tflearn.fully_connected(red, salida, activation='softmax')
    red = tflearn.regression(red, optimizer='sgd', learning_rate=0.05, loss='mean_square')
    modelo = tflearn.DNN(red)
    return modelo

mimodelo = crear_modelo()

#entranimento de la red
mimodelo.fit(trainX, trainY, validation_set=0.3, show_metric=True, batch_size=10, n_epoch=100)

#prediccion usando la red
