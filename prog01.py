# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:15:20 2018

@author: maorc, gcetzalb, esuarez
"""
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as tls
import calendar
import matplotlib.dates as mdates


#file=open("Mensuales_ONI.dat","r")
#a=file.read()
#print(a)


#file.close()

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
    #print(array2)
    #print(array1year)
    #print(array1month)


#if array2.index('"\n"'):
 #   print('hola')
lista = []
lista2 = []
listaGeneral = []
for valor in array2:
    #valor.replace('0.2', "9.9")
    lista.append(valor.rstrip('\n'))



for sal in range(0, 623):
    lista2.append(array1year[sal] +'-'+array1month[sal])

listaGeneral = dict(zip(lista2[1:], lista[1:]))
tupla = listaGeneral.items()
#listaGeneral.append([lista2, lista])
#print(tupla)
df = pd.DataFrame(list(tupla))
df.columns = [ "fecha", "valor"]
#print(df)
xyears = np.linspace(1966, 2017, 6)
tls.plot(df["valor"].astype(float))
tls.title("ONI")
tls.xlabel("Años")
tls.ylabel("Datos ONI")
tls.minorticks_on()
tls.grid()
tls.xticks([0,100,200,300,400,500,600], [1996,1970,1980,1990,2000,2015,2017])
#tls.xlim(1966, 2017)


tls.show()

