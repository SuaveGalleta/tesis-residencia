# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:15:20 2018

@author: maorc, gcetzalb, esuarez
"""
#bibliotecas

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as tls
from scipy.signal import *
from scipy.interpolate import splrep, splev
from numpy import *
from matplotlib.pyplot import *

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

f = 1
#f2 = 1
nueva_list = lista[1:]
data_oni =[]
for item in nueva_list:
    data_oni.append(float(item))

t = np.array(data_oni)

    
x = zeros(len(t))
xmin = zeros(len(t))
xmax = zeros(len(t))

k = 4 #numero del modal

newsi = zeros([k+1, len(x)])
mod = zeros([k,len(x)])

ruido = random.uniform(-0.5, 0.5, 623)
#print(ruido)
signal = sin(2*pi*f*t)+ruido
x = signal
newsi[0,:] = x

for i in range(k):
    x = newsi[i,:]
    data1 = argrelmax(x)
    xmax = x.take(data1)[0]
    tmax = t.take(data1)
    data2 = argrelmin(x)[0]
    xmin = x.take(data2)
    tmin = t.take(data2)

    coef = splrep(tmax, xmax)
    resmax = splev(t,coef)
    coef = splrep(tmin,xmin)
    resmin = splev(t,coef)

    mu = (resmax + resmin)/2
    mod[i,:] = x - mu
    newsi[i+1,:] = x - mod[i,:]






