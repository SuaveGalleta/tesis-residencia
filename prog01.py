# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:15:20 2018

@author: esuarez
"""
#bibliotecas

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as tls
import scipy.io
from PyEMD import EMD
import sympy as sy
import tensorflow as tf
import tflearn as tfl

#limpieza de datos a graficar

#datos IST
array2year=[]
array2month=[]
array3=[]
for line in open('TSI_reconstruc.dat'):
    #array.append(re.findall(pattern,line))
    array2year.append(line[0:4])
    array2month.append(line[4:6])
    
    if line[7]=='-':
        array3.append(line[7:])
        
    else:
        array3.append(line[7:])

lista3 = []
lista4 = []
listaGeneral2 = []
for valor in array3:
    lista3.append(valor.rstrip('\n'))
    lista3.append(valor.replace('\t', ', '))



for sal in range(len(lista3)):
    lista4.append(array2year[sal] +'-'+array2month[sal])


#print(len(lista3))


#creación del dataframe y gráfica

listaGeneral2 = dict(zip(lista4[1:], lista3[1:]))
tupla2 = listaGeneral2.items()
df2 = pd.DataFrame(list(tupla2))
df2.columns = [ "fecha", "valor"]
tls.plot(df2["valor"].astype(float))
tls.title("IST")
tls.xlabel("Años")
tls.ylabel("Datos IST")
tls.minorticks_on()
tls.grid()
#tls.show()



#datos Oni
array1year=[]
array1month=[]
array2=[]
for line in open('Mensuales_ONI.dat'):
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
    lista2.append(array1year[sal] +'-'+array1month[sal])

#creación del dataframe y gráfica

listaGeneral = dict(zip(lista2[1:], lista[1:]))
tupla = listaGeneral.items()
df = pd.DataFrame(list(tupla))
df.columns = [ "fecha", "valor"]
tls.plot(df["valor"].astype(float))
tls.title("ONI")
tls.xlabel("Años")
tls.ylabel("Datos ONI")
tls.minorticks_on()
tls.grid()
tls.xticks([0,100,200,300,400,500,600], [1996,1970,1980,1990,2000,2015,2017])
#tls.show()
#print(lista)

#Descomposición Modal Empirica (DME)

nueva_list = lista3[1:]
data_oni =[]
for item in nueva_list:
    data_oni.append(float(item))
x = np.linspace(0, 10, 407)
signal = np.array(data_oni)
emd = EMD()
IMFS = emd.emd(signal)
#print(IMFS[2])
N = IMFS.shape[0]+2




for i, imf in enumerate(IMFS):
    tls.figure("DME")
    tls.subplot(N,1,i+2)
    tls.plot(x,imf, 'g')
    tls.title("\n IMF "+str(i+1))
    tls.xlabel("Time [s]")

tls.show()

#apartado de las derivadas
#print(IMFS[3])
#resta consecutiva para sacar derivadas
#arracero= [0]
#reversearray= np.append(reversearray,arracero)

def derivadas(dme):
    derivada = []
    reversearray = dme[::-1]
    for line in range(len(reversearray)-1):
        operacion = reversearray[line]-reversearray[line+1]
        derivada.append(operacion)
    
    derivada.append(derivada[0])
    mi_derivada = derivada[::-1]
    
    
    return mi_derivada

#for line in range(len(reversearray)-1):
    #operacion  = reversearray[line]-reversearray[line+1]
    #nuevoarray.append(operacion)

#print(nuevoarray)

#primera derivada
arrayemd = IMFS[3]
nuevoarray =[]
#reversearray = arrayemd[::-1]
primeraderi = derivadas(arrayemd)
#print(primeraderi)


#segunda derivada
segundaderi = derivadas(primeraderi)
#print(segundaderi)
#tls.show()



#datos para el entrenamiento
x = df['fecha']
y = df['valor']

#datos para test
testX = df2['fecha']
testy = df2['valor']

#red neuronal artificial
entradas = 9
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
clases = 10

def modelo_red():
    tf.reset_default_graph()
    #capa de entrada
    red = tfl.input_data([None, entradas])
    #capas ocultas
    red = tfl.fully_connected(red, capa1, activation='ReLU')
    red = tfl.fully_connected(red, capa2, activation='ReLU')
    red = tfl.fully_connected(red, capa3, activation='ReLU')
    red = tfl.fully_connected(red, capa4, activation='ReLU')
    red = tfl.fully_connected(red, capa5, activation='ReLU')
    red = tfl.fully_connected(red, capa6, activation='ReLU')
    red = tfl.fully_connected(red, capa7, activation='ReLU')
    red = tfl.fully_connected(red, capa8, activation='ReLU')
    red = tfl.fully_connected(red, capa9, activation='ReLU')
    red = tfl.fully_connected(red, capa10, activation='ReLU')
    #capa de salida
    red = tfl.fully_connected(red, clases, activation='softmax')
    red = tfl.regression(red, optimizer='sgd', learning_rate=0.1, loss='mean_square')
    modelo = tfl.DNN(red)
    return modelo

#modelo = modelo_red()
#modelo.fit(x, y, validation_set=0.3, show_metric=True, batch_size=9, n_epoch=100)
