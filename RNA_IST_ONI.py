#
# Autor: Eric Alberto Súarez Gallareta
# Creado el 24 de mayo de 2019
#
#Bibliotecas
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as tls
import scipy.io
from PyEMD import EMD
import sympy as sy
import tensorflow as tf
import tflearn
import csv

#preparar datos X
datosv1 = []
for valor in open('X.txt'):
    datosv1.append(valor)
datosv2 = []
for valor in datosv1:
    datosv2.append(valor.strip())
#print(datosv2)
 
#np.asarray(datosv2)
#print(valor_X)
TrainX = np.float32(datosv2)

#print(len(TrainX))

#preparar datos Y
y = []
for valor in open('Y.txt','r'):
    y.append(valor)
valor_y =[]
for valor in y:
    valor_y.append(valor.split())
#print(len(valor_y))

#preparación de datos de test
tx = []
for valor in open('testx.txt','r'):
    tx.append(valor.split())

#print(tx)
TestX = np.float32(tx)

TrainY = np.float32(valor_y)
TrainY = TrainY.reshape(9,467)
TrainX = TrainX.reshape(9,467)
TestX = TestX.reshape(3,467)

#print(TrainY)

entradas = 467
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
salida = 467

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

mimodelo = crear_modelo()

#entranimento de la red
mimodelo.fit(TrainX, TrainY, validation_set=0.3, show_metric=True, batch_size=9, n_epoch=50)

#predicciones
predicciones = np.array(mimodelo.predict(TestX)).argmax(axis = 1)
print(predicciones)
tls.show()
