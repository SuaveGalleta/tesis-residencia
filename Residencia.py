from tkinter import *
from tkinter import filedialog
import re
import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
import matplotlib.pyplot as tls
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import	style
root = Tk()

root.title("Analisis de datos climaticos")
root.resizable(1,1)
style.use("ggplot")

# figure permite dibujar, en este caso permite mostrar la grafica
# add_subplot agregar al canvas en este caso el figure
f = Figure(figsize=(10,5), dpi=100)
a = f.add_subplot(111)
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
    scrollbary = Scrollbar(root)
    scrollbary.pack( side = RIGHT, fill = Y )
    #frame2.config(yscrollcommand=scrollbar.set)
    
    titulo2=Label(frame2, text="Analisis de Datos Climaticos" )
    titulo2.config(font=(15))
    titulo2.grid(padx=5, pady =5, row=0, column=0, columnspan=4)
    
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
            df.columns = [ "fecha", "valor"]
            #print(df)
            #visualizacion de los datos seleccionados
            frame3=Frame(frame2, width=250, height=250)
            frame3.grid(row=3, column=0, padx = 10, pady=5)

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
            for num in df["fecha"]:
                x = x+1
                mylist.insert('','end', "item"+str(x) ,text=num)
                
            #mostrar su respectivo valor
            for value in df["valor"]:
                y=y+1
                mylist.set("item"+str(y),'valor', value)    
            
            namegraph= StringVar()
            name_ejex= StringVar()
            name_ejey=StringVar()
            
            #ver grafica
            def ver_grafica():
                frame5= Frame(frame2, width=500, height=500)
                frame5.grid(row=4, column=0, columnspan=1)
                my_value = df["valor"].astype(float)
                a.plot(my_value)
                canvas = FigureCanvasTkAgg(f, frame5)
                canvas.show()
                canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = True)

            #Realizar y vizualizar graficas
            def realizar_grafica():
                frame4 = Frame(frame2,width=250, height=250)
                frame4.grid(padx=10, pady=10, row=3, column=2)
                

                Label(frame4, text="Parametros para realizar la grafica").grid(row=0, column=0)
                Label(frame4, text="Titulo de la grafica").grid(row=1, column=0)
                
                titlegraph= Entry(frame4, textvariable=namegraph)
                titlegraph.grid(ipadx=5, ipady=5, padx=5, pady=5, row=1, column=1)
                
                Label(frame4, text="Label para el eje x").grid(row=2, column=0)
                ejex= Entry(frame4, textvariable=name_ejex)
                ejex.grid(ipadx=5, ipady=5, padx=5, pady=5, row=2, column=1)
                
                Label(frame4, text="Label para e eje y").grid(row=3, column=0)
                ejey= Entry(frame4, textvariable=name_ejey)
                ejey.grid(ipadx=5, ipady=5, padx=5, pady=5, row=3, column=1)
                Button(frame4, text="Realizar Grafica", command=ver_grafica).grid(padx=5, pady=5, ipadx=5, ipady=5,row=4, column=0)

                

            graph = Button(frame2,text="Ver Grafica", width=20, command=realizar_grafica)
            graph.grid(row=3, column= 1, padx=5, pady=5, ipadx=5, ipady=5)    

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