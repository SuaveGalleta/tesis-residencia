import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 
import pandas as pd
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as tls
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import	style
from PyEMD import EMD
import numpy as np
import re
import scipy.io
from tkinter import simpledialog
import os
import random


#global ruta_new
style.use("ggplot")

# figure permite dibujar, en este caso permite mostrar la grafica
# add_subplot agregar al canvas en este caso el figure
f = Figure(figsize=(10,5), dpi=100)
a = f.add_subplot(111)

class AnalisisClima(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Asignación del titulo de la ventana principal
        self.title("Analisis de Datos Climaticos")

        self.frames={}

        for F in (Inicio, Show_dialog, Show_data, Show_graph, Show_emd):

        
            frame= F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Inicio)
    
    #Mostrar frames , los pone al frente
    def show_frame(self, cont):
         
        frame = self.frames[cont]
        frame.tkraise()
    

#Ventana de inicio
class Inicio(tk.Frame):
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        path = tk.PhotoImage(file = "logo_tec.png")
        logo = tk.Label(self, image= path, width= 100, height=100)
        logo.image = path
        logo.pack(pady = 5,ipady=5)
        welcome = tk.Label(self, text="Bienvenido", font=("Arial",20))
        welcome.pack(pady=5, padx=10,ipady=5, ipadx=10)
        maintitle=tk.Label(self, text="Analisis de datos climaticos", font=("Arial",25))
        maintitle.pack(pady=10, padx=10,ipady=5, ipadx=5)
        boton_iniciar= ttk.Button(self, text="Iniciar",width=20, command=lambda:controller.show_frame(Show_dialog))
        boton_iniciar.pack(padx=5, pady =5, ipadx=5, ipady=5)
        boton_salir =ttk.Button(self, text="Salir", command=self.quit, width=20)
        boton_salir.pack(padx=5, pady =5, ipadx=5, ipady=5)


#ventana para seleccionar archivo
class Show_dialog(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        volver= ttk.Button(self, text="Volver", command=lambda:controller.show_frame(Inicio))
        volver.grid(row=1, column=0, padx=15, pady =5, ipadx=5, ipady=5)
        label = tk.Label(self, text="Seleccionar Archivo", font=("Arial", 20))
        label.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
       

        #funcion para abrir ventana de seleccion del archivo
        def opendialog():
            #ruta.filename=filedialog.askdirectory()
            filename=filedialog.askopenfilename(title='Seleccionar el archivo de informacion', filetypes=(("Archivos Data","*.dat"),("Todos los Archivos","*.*")))   
            messagebox.showinfo("Archivo Seleccionado", "Archivo Seleccionado Correctamente")
            global path
            path=filename
            mi_ruta.config(text=filename)
            abrir_archivo = ttk.Button(self, text="Ver Archivo", command=lambda:controller.show_frame(Show_data), state='enabled')
            abrir_archivo.grid(row=1, column=2, padx=5, pady =5, ipadx=5, ipady=5)
            
           
       
        
           
       
       
        mi_ruta=tk.Label(self, text="Ningun Archivo Seleccionado")
        mi_ruta.grid(row=3, column=0, columnspan=3,padx=5, pady =5, ipadx=5, ipady=5)
        abrir_archivo = ttk.Button(self, text="Ver Archivo", command=lambda:controller.show_frame(Show_data), state='disabled')
        abrir_archivo.grid(row=1, column=2, padx=5, pady =5, ipadx=5, ipady=5)
        boton_select= ttk.Button(self,text="Abrir Archivo", command=opendialog) 
        boton_select.grid(row=1, column=1, padx=5, pady =5, ipadx=5, ipady=5)
       

#ventana para ver los datos
class Show_data(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        #funcion para limpieza de datos y visualizaion de datos
        def ver():

            array1year=[]
            array1month=[]
            array2=[]
            #limpieza de datos
            for line in open(path):
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
                #print(lista)          
            for sal in range(len(lista)):
                lista2.append(array1year[sal] +'-'+array1month[sal])
                #print(lista2)
            #creación del dataframe
            
            listaGeneral = dict(zip(lista2[1:], lista[1:]))
            tupla = listaGeneral.items()
            df = pd.DataFrame(list(tupla))
            df.columns = [ "fecha", "valor"]
            global my_graph
            my_graph = df["valor"].astype(float)

            global new_list
            new_list = lista[1:]
        
            #creacion de la vista de los datos
            mylist = ttk.Treeview(self, columns=("valor"))            
            barra = tk.Scrollbar(self, command=mylist.yview)
            barra.pack( side = tk.RIGHT, fill = tk.Y )
            mylist.configure(yscrollcommand=barra.set)
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

              
        

        head=tk.Label(self,text="Visualizacion de los datos", font=("Arial", 20))
        head.pack(padx=5, pady =5, ipadx=5, ipady=5)
        framebotones=tk.Frame(self)
        framebotones.pack(padx=5, pady =5, ipadx=5, ipady=5)
        #boton regresar
        boton_regresar= ttk.Button(framebotones, text="Volver", command=lambda:controller.show_frame(Show_dialog))
        boton_regresar.grid(row=0, column=0, padx=5, pady =5, ipadx=5, ipady=5)
        #boton para desplegar datos
        boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver) 
        boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)
        #boton ver grafica
        boton_grafica = ttk.Button(framebotones, text="Ver grafica", command=lambda:controller.show_frame(Show_graph))
        boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5) 
        

#ventana mostrar grafica
class Show_graph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        tk.Label(self, text="Grafica", font=("Arial",20)).pack()
        frame_bonito = tk.Frame(self)
        frame_bonito.pack()
        
        
        
       
        #Funcion para realizar la grafica
        def ver_grafica():

            array1year=[]
            array1month=[]
            array2=[]
            #limpieza de datos
            for line in open(path):
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
                #print(lista)          
            for sal in range(len(lista)):
                lista2.append(array1year[sal] +'-'+array1month[sal])
                #print(lista2)
            #creación del dataframe
            
            listaGeneral = dict(zip(lista2[1:], lista[1:]))
            tupla = listaGeneral.items()
            df = pd.DataFrame(list(tupla))
            df.columns = [ "fecha", "valor"]
            global my_graph
            my_graph = df["valor"].astype(float)

            global new_list
            new_list = lista[1:]
        
            file_name = os.path.basename(path)
            index_of_dot = file_name.index('.')
            file_name_without_extension = file_name[:index_of_dot]
            #print (file_name_without_extension)
            a.clear
            a.plot(my_graph)
            a.set_title(file_name_without_extension)
            a.set_ylabel(lista[0])
            a.set_xlabel("Dato")            
            global canvas
            canvas = FigureCanvasTkAgg(f, self)
            canvas.show()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
            limpieza=ttk.Button(frame_bonito, text="Limpiar Pantalla", command=limpiar, state='enabled')
            limpieza.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
           
        
        #boton regresar
        boton_regresar= ttk.Button(frame_bonito, text="Volver", command=lambda:controller.show_frame(Show_data))
        boton_regresar.grid(row=0, column=0, padx=5, pady =5, ipadx=5, ipady=5)

        #boton desplegar la grafica
        
        ttk.Button(frame_bonito,text="Desplegar grafica", command=ver_grafica).grid(row=0, column= 1,padx=5, pady =5, ipadx=5, ipady=5)

        #funcion limpiar pantalla (canvas)
        def limpiar():
            canvas.get_tk_widget().destroy()
            a.clear()
            limpieza=ttk.Button(frame_bonito, text="Limpiar Pantalla", command=limpiar, state='disabled')
            limpieza.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
          


        limpieza=ttk.Button(frame_bonito, text="Limpiar Pantalla", command=limpiar, state='disabled')
        limpieza.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
        ttk.Button(frame_bonito,text="Aplicar EMD", command=lambda:controller.show_frame(Show_emd)).grid(row=0, column= 3,padx=5, pady =5, ipadx=5, ipady=5)


#ventana para ver el EMD
class Show_emd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)     

        tk.Label(self, text="Descompoición Modal Empirica",font=("Arial", 20)).pack(padx=5, pady =5, ipadx=5, ipady=5) 
        

        def desplegar_emd():
            array1year=[]
            array1month=[]
            array2=[]
            #limpieza de datos
            for line in open(path):
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
                #print(lista)          
            for sal in range(len(lista)):
                lista2.append(array1year[sal] +'-'+array1month[sal])
                #print(lista2)
            #creación del dataframe
            
            listaGeneral = dict(zip(lista2[1:], lista[1:]))
            tupla = listaGeneral.items()
            df = pd.DataFrame(list(tupla))
            df.columns = [ "fecha", "valor"]
            global my_graph
            my_graph = df["valor"].astype(float)

            global new_list
            new_list = lista[1:]

            dataoni = []
            for item in new_list:
                dataoni.append(float(item))
            signal = np.array(dataoni)
            emd = EMD()
            IMFS = emd.emd(signal)
            funcion= tk.StringVar()
            funcion.set("Seleccione la Descomposición")

            opciones = []
            for line in range(len(IMFS)):
                opciones.append(line)
                #print (line)            
            
            dropselect = ttk.OptionMenu(self, funcion, *opciones)
            dropselect.pack(padx=5, pady =5, ipadx=5, ipady=5)

            ttk.Button(parejo, text="Desplegar DME", command=desplegar_emd, state='disabled').grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)


           

            
            def ver_dme():
                global seleccion
                seleccion= int(funcion.get())
                global my_canvas           
                a.clear()        
                a.plot(IMFS[seleccion])
                a.set_title("IMF "+str(seleccion))
                a.set_xlabel("Tiempo [s]")
                canvas2 = FigureCanvasTkAgg(f, self)
                canvas2.show()
                canvas2.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                my_canvas = canvas2
           

            def prueba():
                file_name = os.path.basename(path)
                index_of_dot = file_name.index('.')
                file_name_without_extension = file_name[:index_of_dot]
                #print (file_name_without_extension)
                global mycanvas3
                a.clear()
                a.plot(IMFS[seleccion])
                a.plot(my_graph)
                a.set_title(file_name_without_extension + " y " + "IMF "+str(seleccion) )
                canvas3 = FigureCanvasTkAgg(f, self)
                canvas3.show()
                canvas3.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                mycanvas3 = canvas3
            
            
            def clear2():
                
                my_canvas.get_tk_widget().destroy()
                mycanvas3.get_tk_widget().destroy() 
                a.clear()     
            
            
                
            
            my_frame_grid=tk.Frame(self)
            my_frame_grid.pack() 
            ttk.Button(my_frame_grid, text="Desplegar grafica", command=ver_dme).grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
            ttk.Button(my_frame_grid, text="Limpiar Pantalla", command=clear2).grid(row=0, column=1,padx=5, pady =5, ipadx=5, ipady=5)
            ttk.Button(my_frame_grid, text="Comparacion con los datos", command=prueba).grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
            

        parejo=tk.Frame(self)
        parejo.pack()
        ttk.Button(parejo, text="Volver", command=lambda:controller.show_frame(Show_graph)).grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
        ttk.Button(parejo, text="Desplegar DME", command=desplegar_emd).grid(row=0, column=1,padx=5, pady =5, ipadx=5, ipady=5)
    



    

app= AnalisisClima()
app.mainloop()

