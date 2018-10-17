from tkinter import *
from tkinter import filedialog
import re
import pandas as pd
import matplotlib.pyplot as tls
root = Tk()

root.title("Analisis de datos climaticos")
root.resizable(1,1)

#comando para salir
def salir():
    root.quit()





#comando abrir nueva ventana
def cargar_archivos():
    #ventana de la seleccion de datos climaticos
    abrir_data=Tk()
    abrir_data.title("Analisis de datos climaticos")
    abrir_data.resizable(1,1)
    frame2 = Frame(abrir_data, width=250, height=250)
    frame2.grid(row=0, column=1)
    titulo2=Label(frame2, text="Seleccione el archivo" )
    titulo2.config(font=(15))
    titulo2.grid(padx=5, pady =5, row=0, column=0)
    
    #abrir cuadro de seleccion del archivo
    def abrir_dialog():
        ruta=filedialog.askopenfilename(title='Seleccionar el archivo de informacion', filetypes=(("Archivos Data","*.dat"),("Todos los Archivos","*.*")))
        pathlabel=Label(frame2)
    
        pathlabel.config(text=ruta)
        pathlabel.grid(row=1,column=0)

        #ver registros de la ruta seleccionada
        def ver_mas():
            array1year=[]
            array1month=[]
            array2=[]
            #limpieza de datos
            for line in open(ruta):
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

            #creación del dataframe
            listaGeneral = dict(zip(lista2[1:], lista[1:]))
            tupla = listaGeneral.items()
            df = pd.DataFrame(list(tupla))
            print(df)        
        
        ver_reg= Button(frame2, text="Ver registros", width=20, command=ver_mas)
        ver_reg.grid(padx=5, pady=5, ipadx=5, ipady=5,row=2, column=1)
         

    file_choosser= Button(frame2, text="Seleccionar Archivo" ,width=20, command=abrir_dialog)
    file_choosser.grid(padx=5, pady=5, ipadx=5, ipady=5, row=1, column=1)
   
    
    
    root.iconify()
















# ventana Inicio
frame = Frame(root, width = 250, height = 250)
frame.pack(fill = "both", expand = 1)
path = PhotoImage(file = "logo_tec.png")
logo = Label(frame, image= path, width= 100, height=100)
logo.pack(pady = 5,ipady=5)
etiquetatitulo = Label(frame, text= "Bienvenidos")
etiquetatitulo.config(font=(25))
etiquetatitulo.pack(pady = 5,ipady=5)
etiquetatitulo2 = Label(frame, text="Sistema para el analisis de datos climaticos")
etiquetatitulo2.config(font=(20))
etiquetatitulo2.pack(padx=5, pady = 5, ipadx=5,ipady=5)
Button(frame, text="Iniciar", width=20, command=cargar_archivos).pack(padx=5, pady =10)
Button(frame, text="Salir", width=20, command=salir).pack(padx=5, pady =10)




root.mainloop()









