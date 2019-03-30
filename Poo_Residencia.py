#bibliotecas
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 
import pandas as pd
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as tls
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
import csv


#mejora la visualización de las gráficas
style.use("ggplot")

# figure permite dibujar, en este caso permite mostrar la grafica
# add_subplot agregar al canvas en este caso el figure
f = Figure(figsize=(10,5), dpi=100)
a = f.add_subplot(111)


class AnalisisClima(tk.Tk):
    #todo lo que este dentro de este método se ejecuta cuando se compila el código
    def __init__(self):
        tk.Tk.__init__(self)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Asignación del titulo de la ventana principal
        self.title("Análisis de Datos Climáticos")

        self.frames={}
        #ciclo for que recorre los frames , dentro del parentesis se agregan los frames para cargarlos
        for F in (Inicio, Show_dialog, Show_data):

        
            frame= F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        #mostar la pantalla cuando se inicie el sistema
        self.show_frame(Inicio)
    
    #Mostrar frames , los pone al frente
    def show_frame(self, cont):
         
        frame = self.frames[cont]
        frame.tkraise()
    

#Frame de inicio
class Inicio(tk.Frame):
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        #agrega una imagen al frame
        path = tk.PhotoImage(file = "logo_tec.png")
        logo = tk.Label(self, image= path, width= 100, height=100)
        logo.image = path
        logo.pack(pady = 5,ipady=5)
        #agrega un label al frame
        #label de bienvenida
        welcome = tk.Label(self, text="Bienvenido", font=("Arial",20))
        welcome.pack(pady=5, padx=10,ipady=5, ipadx=10)
        #label de título del software
        maintitle=tk.Label(self, text="Análisis de datos climáticos", font=("Arial",25))
        maintitle.pack(pady=10, padx=10,ipady=5, ipadx=5)
        #botón para iniciar el software y todos los procesos
        boton_iniciar= ttk.Button(self, text="Iniciar",width=20, command=lambda:controller.show_frame(Show_dialog))
        boton_iniciar.pack(padx=5, pady =5, ipadx=5, ipady=5)
        #botón para salir o cerrar la aplicación
        boton_salir =ttk.Button(self, text="Salir", command=self.quit, width=20)
        boton_salir.pack(padx=5, pady =5, ipadx=5, ipady=5)


#Frame para seleccionar archivo
class Show_dialog(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)


        #función para pasar a la siguiente ventana
        def siguiente():
            #botón para ir al siguiente frame
            #se desactiva cuando se pasa al siguiente frame
            abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=siguiente, state='disabled')
            abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
            #label vuelve a pasar a su estado original cuando se pasa al siguiente frame
            mi_ruta.config(text="Ningun Archivo Seleccionado")
            #comando para pasar al frame que se desee
            controller.show_frame(Show_data)
           

        #función del botón volver 
        def forzar():
            #botón para ir al frame anterior
            #se desactiva cuando se pasa al frame anterior
            abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=lambda:controller.show_frame(Show_data), state='disabled')
            abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
            #comando para pasar al frame que se desee
            controller.show_frame(Inicio)
            #label vuelve a pasar a su estado original cuando se pasa al frame anterior
            mi_ruta.config(text="Ningun Archivo Seleccionado")


        #botón volver del frame selección del archivo
        volver= ttk.Button(self, text="Volver", command=forzar)
        volver.pack(padx=15, pady =5, ipadx=5, ipady=5)
        #label del título del frame
        label = tk.Label(self, text="Abrir Archivo", font=("Arial", 20))
        label.pack(padx=5, pady =5, ipadx=5, ipady=5)
        #frames extras
        framedialog = tk.Frame(self)
        framedialog.pack()
        framelabel = tk.Frame(self)
        framelabel.pack()
    
 
       
        
        #funcion para abrir ventana de seleccion del archivo
        def opendialog():
            #ruta.filename=filedialog.askdirectory()
            filename=filedialog.askopenfilename(title='Seleccionar el archivo de informacion', filetypes=(("Archivos Data","*.dat"),("Todos los Archivos","*.*")))   
            
            global path
            path=filename
            #condición para verificar si esta vacío la variable path
            if(path == "" or not path):
                #mensaje de error
                messagebox.showerror("Error", "Selecciones un archivo para continuar")
                #descativa botón de ver el archivo
                abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=siguiente, state='disabled')
                abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
                #pone el label a su estado original
                mi_ruta.config(text="Ningun Archivo Seleccionado")

            else:
                
                #de la ruta con el archivo solo toma el nombre del archivo
                file_name = os.path.basename(path)
                #el label toma el nombre del archivo
                mi_ruta.config(text=file_name)
                #se activa el botón ver archivo
                abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=siguiente, state='enabled')
                abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
           
            
            
           
           
       
        
           
        #label
        label_title = tk.Label(framelabel, text="Archivo Seleccionado: ")
        label_title.grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
        #label que cambia segun el archivo seleccionado 
        mi_ruta=tk.Label(framelabel, text="Ningun Archivo Seleccionado")
        mi_ruta.grid(row=0, column=1,padx=5, pady =5, ipadx=5, ipady=5)

       
        

        #botón ver archivo
        abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=lambda:controller.show_frame(Show_data), state='disabled')
        abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
        #botón para abrir el dialogo de selección del archivo
        boton_select= ttk.Button(framedialog,text="Seleccionar Archivo", command=opendialog) 
        boton_select.grid(row=0, column=0, padx=5, pady =5, ipadx=5, ipady=5)
       

#Frame para ver los datos
class Show_data(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #frames extras
        framedme = tk.Frame(self)
        frametree = tk.Frame(self)
        framevolver = tk.Frame(self)
        #funcion para limpieza de datos y visualizaion de datos
        def ver():
            for widget in frametree.winfo_children():
                widget.destroy()
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
                          
            for sal in range(len(lista)):
                lista2.append(array1year[sal] +'-'+array1month[sal])

            #creación del dataframe
            
            listaGeneral = dict(zip(lista2[1:], lista[1:]))
            tupla = listaGeneral.items()
            df = pd.DataFrame(list(tupla))
            df.columns = [ "fecha", "valor"]
            global my_graph
            my_graph = df["valor"].astype(float)

            global new_list
            new_list = lista[1:]
        
            #Tabla
            #creacion de la vista de los datos
            global mylist
            mylist = ttk.Treeview(frametree, columns=("valor"))            
            barra = tk.Scrollbar(frametree, command=mylist.yview)
            barra.pack( side = tk.RIGHT, fill = tk.Y )
            mylist.configure(yscrollcommand=barra.set)
            mylist.pack()
            
            #cabecera de la tabla
            mylist.heading("#0",text=lista2[0])
            mylist.heading("valor",text=lista[0])
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
            
            
            

              
        
         #función del botón regresar
        def regresar():
            controller.show_frame(Show_dialog)
            for widget in frametree.winfo_children():
                widget.destroy()

        #frame extra
        framevolver = tk.Frame(self)
        framevolver.pack()
        #botón regresar
        boton_regresar= ttk.Button(framevolver, text="Volver", command=regresar)
        boton_regresar.grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
        #label del título del frame
        head=tk.Label(self,text="Visualización de los datos", font=("Arial", 20))
        head.pack(padx=5, pady =5, ipadx=5, ipady=5)
        #frame extra que contiene todos los botones y se inicializan los otros frames
        framebotones=tk.Frame(self)
        framebotones.pack(padx=5, pady =5, ipadx=5, ipady=5)
        framedme.pack()
        frametree.pack()
       
        #boton para desplegar datos
        boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver) 
        boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)


       #Función para realizar la gráfica
        def ver_grafica():
            for widget in frametree.winfo_children():
                widget.destroy()
          
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
                          
            for sal in range(len(lista)):
                lista2.append(array1year[sal] +'-'+array1month[sal])
                
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
            
            #se limpia la gráfica
            a.clear()
            #se grafican los datos
            a.plot(my_graph)
            #se agrgan leyenda para la gráfica
            a.legend(["Datos "+lista[0]])
            #se agrega título para la gráfica
            a.set_title(file_name_without_extension)
            #se agrega label a los ejes x y y
            a.set_ylabel(lista[0])
            a.set_xlabel("Cantidad de datos")            
            global canvas
            #se agrega la gráfica al canvas
            canvas = FigureCanvasTkAgg(f, frametree)
            canvas.draw()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
            #barra de opciones para un mejor análisis de la gráfica
            toolbar = NavigationToolbar2Tk(canvas,frametree)
            toolbar.update()
            toolbar.pack()
            
            

        #boton ver grafica
        boton_grafica = ttk.Button(framebotones, text="Ver gráfica", command=ver_grafica)
        boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5) 
                 
        

        #función para aplicar el dme
        def ver_dme2():
            for widget in frametree.winfo_children():
                widget.destroy()
            
          
            #botón para volver
            boton_regresar= ttk.Button(framevolver, text="Volver", command=regresar, state='disabled')
            boton_regresar.grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
            #botón para desplegar datos
            boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver, state='disabled') 
            boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)
            #botón para aplicar el dme
            ttk.Button(framebotones,text="Aplicar DME" ,command=ver_dme2, state='disabled').grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)
            #botón ver grafica
            boton_grafica = ttk.Button(framebotones, text="Ver gráfica", command=ver_grafica, state='disabled')
            boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5) 



            
                



            #crea una nueva ventana y la pone de frente
            self.show_dme = tk.Toplevel()
            #frames extras
            selectframe = tk.Frame(self.show_dme)
            my_frame_grid=tk.Frame(self.show_dme)
            frametodo= tk.Frame(self.show_dme)

            #función del botón volver
            def borrar():
                #botón volver
                boton_regresar= ttk.Button(framevolver, text="Volver", command=regresar, state='enabled')
                boton_regresar.grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
                #boton para desplegar datos
                boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver, state='enabled') 
                boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)
                #botón aplicar dme
                ttk.Button(framebotones,text="Aplicar DME" ,command=ver_dme2, state='enabled').grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)
                #boton ver grafica
                boton_grafica = ttk.Button(framebotones, text="Ver gráfica", command=ver_grafica, state='enabled')
                boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
                #destruye todo lo que contenga el frame
                for widget in frametodo.winfo_children():
                    widget.destroy()
            
                for widget in selectframe.winfo_children():
                    widget.destroy()
            
                for widget in my_frame_grid.winfo_children():
                    widget.destroy()
                
                #destruye la ventana
                self.show_dme.destroy()

            #botón volver
            ttk.Button(self.show_dme,text="Volver", command=borrar).pack(padx=5, pady =5, ipadx=5, ipady=5)
            #label del título de la nueva ventana
            tk.Label(self.show_dme, text="Descomposición Modal Empírica",font=("Arial", 20)).pack(padx=5,   pady =5, ipadx=5, ipady=5)
            #función del boton de salir que se encuentra en la ventana
            def on_exit():
                #volver botón activar
                boton_regresar= ttk.Button(framevolver, text="Volver", command=regresar, state='enabled')
                boton_regresar.grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
                #Desplegar botón activar
                boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver, state='enabled') 
                boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)
                #botón aplicar dme
                ttk.Button(framebotones,text="Aplicar DME" ,command=ver_dme2, state='enabled').grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)
                #boton ver grafica
                boton_grafica = ttk.Button(framebotones, text="Ver gráfica", command=ver_grafica, state='enabled')
                boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
                #destruye la ventana creada
                self.show_dme.destroy()

            #asiganción de la función al botón de salir (-),(<>),--->(x)
            self.show_dme.protocol("WM_DELETE_WINDOW", on_exit)




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
                    
                    
            #Aplicación del DME
            lista = []
            lista2 = []
            listaGeneral = []
            for valor in array2:
                lista.append(valor.rstrip('\n'))
                          
            for sal in range(len(lista)):
                lista2.append(array1year[sal] +'-'+array1month[sal])
                
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
            funcion= tk.StringVar(selectframe)
            funcion.set("Seleccione la Descomposición")

            #pone todas las descomposiciones en una lista
            opciones = []
            for line in range(len(IMFS)):
                opciones.append(line)
            
            global dropselect
            #cuadro de selección con todas las descomposiciones
            dropselect = ttk.OptionMenu(selectframe, funcion, *opciones)
            dropselect.pack(padx=5, pady =5, ipadx=5, ipady=5)
            
            #función para graficar el dme seleccionado
            def ver_dme():
                global seleccion
                seleccion= funcion.get()
                #función para verificar que no este vacío el campo de selección
                if(seleccion=="Seleccione la Descomposición"):
                    messagebox.showerror("Error", "Selecciona una DME para visualizar", parent=self.show_dme)
                else:
                    #limpia el frame
                    for widget in frametodo.winfo_children():
                        widget.destroy()
                    global my_canvas
                    #limpia la gráfica           
                    a.clear()
                    #gráfica el dme seleccionado        
                    a.plot(IMFS[int(seleccion)])
                    #agrega leyenda a la gráfica
                    a.legend(["IMF "+str(seleccion)])
                    #asigan título a la gráfica
                    a.set_title("DME "+str(seleccion))
                    #pone título a los ejes
                    a.set_xlabel("Tiempo [s]")
                    #pone la gráfica dentro del canvas
                    canvas2 = FigureCanvasTkAgg(f, frametodo)
                    canvas2.draw()
                    canvas2.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                    #agrega barra de herraminetas para la gráfica
                    toolbar = NavigationToolbar2Tk(canvas2,frametodo)
                    toolbar.update()
                    toolbar.pack()
                    my_canvas = canvas2

            #función para comparación de datos y dme
            def prueba():
                #se obtiene la selección del usuario
                seleccion= funcion.get()
                #se verifica que no este vacío el cuadro de selección
                if (seleccion == "Seleccione la Descomposición"):
                    messagebox.showerror("Error", "Selecciona una DME para visualizar", parent=self.show_dme)
                else:
                    #limpia el frame
                    for widget in frametodo.winfo_children():
                        widget.destroy()
                    file_name = os.path.basename(path)
                    index_of_dot = file_name.index('.')
                    file_name_without_extension = file_name[:index_of_dot]
                    #print (file_name_without_extension)
                    global mycanvas3
                  
                    #limpia gráfica
                    a.clear()
                    #crea la gráfica con los datos
                    a.plot(my_graph)
                    a.plot(IMFS[int(seleccion)])
                    #agrega leyenda dde los datos
                    a.legend(["Datos "+lista[0],"IMF "+str(seleccion)])
                    #agrega título a la gráfica
                    a.set_title(file_name_without_extension + " y " + "DME "+str(seleccion) )
                    #agrega la gráfica al canvas
                    canvas3 = FigureCanvasTkAgg(f, frametodo)
                    canvas3.draw()
                    canvas3.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                    #barra de herraminentas para la gráfica
                    toolbar = NavigationToolbar2Tk(canvas3,frametodo)
                    toolbar.update()
                    toolbar.pack()
                    #canvas3._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                    mycanvas3 = canvas3

            #función para guardar el dme
            def guardar():
                #se obtiene la selección del usuario
                my_dme= funcion.get()
                #condición para verificar si esta vacío
                if (my_dme == "Seleccione la Descomposición"):
                    messagebox.showerror("Error", "Selecciona una DME para guardar", parent=self.show_dme)
                else:
                    #limpiar frame
                    for widget in frametodo.winfo_children():
                        widget.destroy()
                    messagebox.showinfo("Correcto", "Archivo Guardado con exito", parent=self.show_dme)
                    #crea el archivo
                    with open('DME '+my_dme+'.dat', 'w') as f:
                        f.write("Pos    IMFS "+my_dme+"\n")
                        posicion=0
                        for i in IMFS[int(my_dme)]:
                            posicion=posicion+1
                            pos = str(posicion)
                            new_pos = pos.zfill(4)
                            new_pos = pos.rjust(4,'0')
                            f.writelines(new_pos+"    "+str(i)+"\n")
                        f.close()
                        
            selectframe.pack()
            
            my_frame_grid.pack() 
            #botón desplegar gráfica
            ttk.Button(my_frame_grid, text="Desplegar grafica", command=ver_dme).grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
            #botón comparación de datos
            ttk.Button(my_frame_grid, text="Comparacion con los datos", command=prueba).grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
            #botón de guardar datos
            ttk.Button(my_frame_grid, text="Guardar DME", command=guardar).grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)
            frametodo.pack()

          
        
        #botón de aplicar dme
        ttk.Button(framebotones,text="Aplicar DME" ,command=ver_dme2).grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)


    


   
#llamamos al método
app= AnalisisClima()
#hacemos que se ejecute la biblioteca tkinter para crear la ventana
app.mainloop()

