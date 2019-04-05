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

array1year=[]
array1month=[]
array2=[]
for line in open('Mensuales_ONI.dat'):
    #array.append(re.findall(pattern,line))
    array1year.append(line[0:4])
    array1month.append(line[4:6])
    
    if line[7]=='-':
        array2.append(line[7:11])
        
    else:
        array2.append(line[7:10])
  
lista = []
lista2 = []
listaGeneral = []
for valor in array2:
    lista.append(valor.rstrip('\n'))



for sal in range(0, 623):
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

#Descomposición Modal Empirica (DME)

nueva_list = lista[1:]
data_oni =[]
for item in nueva_list:
    data_oni.append(float(item))
x = np.linspace(0, 10, 623)
signal = np.array(data_oni)
emd = EMD()
IMFS = emd.emd(signal)
#print(IMFS[2])
#N = IMFS.shape[0]+1

"""
for i, imf in enumerate(IMFS):
    tls.figure("DME")
    tls.subplot(N,1,i+2)
    tls.plot(x,imf, 'g')
    tls.title("IMF "+str(i+1))
    tls.xlabel("Time [s]")
"""

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
print(primeraderi)


#segunda derivada
segundaderi = derivadas(primeraderi)
#print(segundaderi)
#tls.show()

#red neuronal artificial
entradas
capa1 = 9
  

