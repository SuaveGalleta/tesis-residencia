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
import math
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
x1=array1year[1:]




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


#preparacion de datos IST
#datos de IST
array2year=[]
array2month=[]
array3=[]

for line in datos_IST:
    #array.append(re.findall(pattern,line))
    array2year.append(line[0:4])
    array2month.append(line[4:6])
    
    if line[7]=='-':
        array3.append(line[7:])
        
    else:
        array3.append(line[7:])
  
lista1 = []
lista3 = []
listaGeneral1 = []
for valor in array3:
    lista1.append(valor.rstrip('\n'))



for sal in range(len(lista1)):
    lista3.append(array2year[sal]+array2month[sal])


listaGeneral1 = dict(zip(lista3[1:], lista1[1:]))
tupla2 = listaGeneral1.items()
df2 = pd.DataFrame(list(tupla2))
df2.columns = [ "fecha", "valor"]
y2 = df2['valor'].astype(float)
x2 = array2year[1:]

#aplicacicion DME
los_dme = dme_function(y2)
#dme utilizados 5,6,7

#dme 5
#primera derivada
primera_deri_dme5 = derivar(los_dme[5])
#segunda derivada
segunda_deri_dme5 = derivar(primera_deri_dme5)

#dme 6'
#primera derivada
primera_deri_dme6 = derivar(los_dme[6])
#segunda derivada
segunda_deri_dme6 = derivar(primera_deri_dme6) 

#dme7
#primera derivada
primera_deri_dme7 = derivar(los_dme[7])
#segunda derivada
segunda_deri_dme7 = derivar(primera_deri_dme7)


array_train = los_dme[5]+primera_deri_dme5+segunda_deri_dme5+los_dme[6]+primera_deri_dme6+segunda_deri_dme6+los_dme[7]+primera_deri_dme7+segunda_deri_dme7










#creación de la red neuronal artificial
#preparación de los datos para el entrenamiento
trainY = np.float32(array_train)
trainX = np.float32(x2)

trainX  = trainX.reshape(37,11)

trainY = trainY.reshape(37,11)

#creacion de las neuronas para cada capa
entradas = 11
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
salida = 11

#creación del modelo de la RNA
def crear_modelo():
    tf.reset_default_graph()
    red = tflearn.input_data([None, entradas])
    red = tflearn.fully_connected(red, capa1, activation='tanh')
    red = tflearn.fully_connected(red, capa2, activation='tanh')
    red = tflearn.fully_connected(red, capa3, activation='tanh')
    red = tflearn.fully_connected(red, capa4, activation='tanh')
    red = tflearn.fully_connected(red, capa5, activation='tanh')
    red = tflearn.fully_connected(red, capa6, activation='tanh')
    red = tflearn.fully_connected(red, capa7, activation='tanh')
    red = tflearn.fully_connected(red, capa8, activation='tanh')
    red = tflearn.fully_connected(red, capa9, activation='tanh')
    red = tflearn.fully_connected(red, capa10, activation='tanh')
    red = tflearn.fully_connected(red, salida, activation='linear')
    red = tflearn.regression(red, optimizer='adam', learning_rate=0.05, loss='mean_square')
    modelo = tflearn.DNN(red)
    return modelo


#relu
#softmax
#momentum
#0.01
#16%


#tanh
#linear
#adam
#0.01 o 0.005
#con 0.01 = 20%
#con 0.05 = 17%

#softsign
#softplus
#Ftrl
#0.01
#22%
#batch = none
#validation = 0.1

mimodelo = crear_modelo()

#entranimento de la red
mimodelo.fit(trainX, trainY, validation_set=0.3, show_metric=True, batch_size=None, n_epoch=100)

#prediccion usando la red
