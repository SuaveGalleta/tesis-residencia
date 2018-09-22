# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:15:20 2018

@author: maorc, gcetzalb
"""
import re
import numpy as np
import pandas as pd

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

listaGeneral.append([lista2, lista])
print(listaGeneral)
#df = pd.DataFrame(np.array(listaGeneral))
#print(df)