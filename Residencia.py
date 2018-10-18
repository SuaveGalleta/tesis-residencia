from tkinter import *
from tkinter import filedialog
import re
import pandas as pd
import matplotlib.pyplot as tls
from tkinter import ttk
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
            #visualizacion de los datos seleccionados
            frame3=Frame(frame2, width=250, height=250)
            frame3.grid(row=3, column=0, padx = 10, pady=5)
             
            """
            scrollbar = Scrollbar(frame3)
            scrollbar.pack( side = RIGHT, fill = Y )
            mylist= Listbox(frame3, yscrollcommand= scrollbar.set)
            for line in tupla:
                mylist.insert(END,line)
            mylist.pack()
            scrollbar.config(command=mylist.yview)
            """
            #creacion de los scrollbars
            scrollbar = Scrollbar(frame3)
            scrollbar.pack( side = RIGHT, fill = Y )
            scrollbarx= Scrollbar(frame3, orient=HORIZONTAL)
            scrollbarx.pack(side= BOTTOM, fill = X )
            #creacion del treeview y su configuracion
            mylist = ttk.Treeview(frame3, yscrollcommand=scrollbar.set, xscrollcommand=scrollbarx.set, columns=("valor"))
            mylist.pack()
            mylist.heading("#0",text="Fecha")
            mylist.heading("valor",text="Valor")
            x=-1
            y=-1
            #Mostrar fechas en el treeview
            for num in df[0]:
                x = x+1
                mylist.insert('','end', "item"+str(x) ,text=num)
                
            """
            for key in df[0]:
                #print(key)
                x = x+1
                mylist.set(x,'fecha', key)
            """
            #mostrar su respectivo valor
            for value in df[1]:
                y=y+1
                mylist.set("item"+str(y),'valor', value)    

            """
            for line in range(len(df)):
                for line2 in df.head():
                    mylist.set(line,'Fecha',line2)
            """
            """
            for line in range(len(df)):
                for value in lista2 :
                    mylist.set("item"+str(line),'fecha', value)
            """    

        #boton para vizualizar los registros del archivo seleccionado 
        ver_reg= Button(frame2, text="Ver registros", width=20, command=ver_mas)
        ver_reg.grid(padx=5, pady=5, ipadx=5, ipady=5,row=2, column=1)
         
    #boton para seleccionar el archivo climatico a analizar
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

