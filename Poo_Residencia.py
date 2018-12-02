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
import csv


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
        self.title("Análisis de Datos Climáticos")

        self.frames={}

        for F in (Inicio, Show_dialog, Show_data):

        
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
        maintitle=tk.Label(self, text="Análisis de datos climáticos", font=("Arial",25))
        maintitle.pack(pady=10, padx=10,ipady=5, ipadx=5)
        boton_iniciar= ttk.Button(self, text="Iniciar",width=20, command=lambda:controller.show_frame(Show_dialog))
        boton_iniciar.pack(padx=5, pady =5, ipadx=5, ipady=5)
        boton_salir =ttk.Button(self, text="Salir", command=self.quit, width=20)
        boton_salir.pack(padx=5, pady =5, ipadx=5, ipady=5)


#ventana para seleccionar archivo
class Show_dialog(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)



        def siguiente():
            abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=siguiente, state='disabled')
            abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
            mi_ruta.config(text="Ningun Archivo Seleccionado")
            controller.show_frame(Show_data)
           


        def forzar():
            abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=lambda:controller.show_frame(Show_data), state='disabled')
            abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
            controller.show_frame(Inicio)
            mi_ruta.config(text="Ningun Archivo Seleccionado")



        volver= ttk.Button(self, text="Volver", command=forzar)
        volver.pack(padx=15, pady =5, ipadx=5, ipady=5)
        label = tk.Label(self, text="Abrir Archivo", font=("Arial", 20))
        label.pack(padx=5, pady =5, ipadx=5, ipady=5)
        framedialog = tk.Frame(self)
        framedialog.pack()
        framelabel = tk.Frame(self)
        framelabel.pack()
    
 
       
        
        #funcion para abrir ventana de seleccion del archivo
        def opendialog():
            #ruta.filename=filedialog.askdirectory()
            filename=filedialog.askopenfilename(title='Seleccionar el archivo de informacion', filetypes=(("Archivos Data","*.dat"),("Todos los Archivos","*.*")))   
            #messagebox.showinfo("Archivo Seleccionado", "Archivo Seleccionado Correctamente")
            global path
            path=filename

            if(path == "" or not path):
                messagebox.showerror("Error", "Selecciones un archivo para continuar")
                abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=siguiente, state='disabled')
                abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
                mi_ruta.config(text="Ningun Archivo Seleccionado")

                #mi_ruta=tk.Label(framelabel, text="Ningun Archivo Seleccionado")
                #mi_ruta.grid(row=0, column=1,padx=5, pady =5, ipadx=5, ipady=5)
            else:
               

                file_name = os.path.basename(path)
                mi_ruta.config(text=file_name)
                abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=siguiente, state='enabled')
                abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
           
            
            
           
           
       
        
           

        label_title = tk.Label(framelabel, text="Archivo Seleccionado: ")
        label_title.grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
               
        mi_ruta=tk.Label(framelabel, text="Ningun Archivo Seleccionado")
        mi_ruta.grid(row=0, column=1,padx=5, pady =5, ipadx=5, ipady=5)

       
        


        abrir_archivo = ttk.Button(framedialog, text="Ver Archivo Seleccionado", command=lambda:controller.show_frame(Show_data), state='disabled')
        abrir_archivo.grid(row=0, column=1, padx=5, pady =5, ipadx=5, ipady=5)
        boton_select= ttk.Button(framedialog,text="Seleccionar Archivo", command=opendialog) 
        boton_select.grid(row=0, column=0, padx=5, pady =5, ipadx=5, ipady=5)
       

#ventana para ver los datos
class Show_data(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        framedme = tk.Frame(self)
        frametree = tk.Frame(self)
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
            global mylist
            mylist = ttk.Treeview(frametree, columns=("valor"))            
            barra = tk.Scrollbar(frametree, command=mylist.yview)
            barra.pack( side = tk.RIGHT, fill = tk.Y )
            mylist.configure(yscrollcommand=barra.set)
            mylist.pack()
            
            
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
            
            
            

              
        
         #boton regresar
        def regresar():
            controller.show_frame(Show_dialog)
            for widget in frametree.winfo_children():
                widget.destroy()



        boton_regresar= ttk.Button(self, text="Volver", command=regresar)
        boton_regresar.pack(padx=5, pady =5, ipadx=5, ipady=5)
        head=tk.Label(self,text="Visualización de los datos", font=("Arial", 20))
        head.pack(padx=5, pady =5, ipadx=5, ipady=5)
        framebotones=tk.Frame(self)
        framebotones.pack(padx=5, pady =5, ipadx=5, ipady=5)
        framedme.pack()
        frametree.pack()
       
        #boton para desplegar datos
        boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver) 
        boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)


       #Funcion para realizar la grafica
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
            a.clear()
            a.plot(my_graph)
            a.legend(["Datos "+lista[0]])
            a.set_title(file_name_without_extension)
            a.set_ylabel(lista[0])
            a.set_xlabel("Cantidad de datos")            
            global canvas
            canvas = FigureCanvasTkAgg(f, frametree)
            canvas.show()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
            toolbar = NavigationToolbar2TkAgg(canvas,frametree)
            toolbar.update()
            toolbar.pack()
            
            

        #boton ver grafica
        boton_grafica = ttk.Button(framebotones, text="Ver gráfica", command=ver_grafica)
        boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5) 
                 
        


        def ver_dme2():
            for widget in frametree.winfo_children():
                widget.destroy()
            
          

            boton_regresar= ttk.Button(framebotones, text="Volver", command=regresar, state='disabled')
            boton_regresar.grid(row=0, column=0, padx=5, pady =5, ipadx=5, ipady=5)
            #boton para desplegar datos
            boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver, state='disabled') 
            boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)
            ttk.Button(framebotones,text="Aplicar DME" ,command=ver_dme2, state='disabled').grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)
            #boton ver grafica
            boton_grafica = ttk.Button(framebotones, text="Ver gráfica", command=ver_grafica, state='disabled')
            boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5) 



            
                




            self.show_dme = tk.Toplevel()
         
            selectframe = tk.Frame(self.show_dme)
            my_frame_grid=tk.Frame(self.show_dme)
            frametodo= tk.Frame(self.show_dme)

            def borrar():
                boton_regresar= ttk.Button(framebotones, text="Volver", command=regresar, state='enabled')
                boton_regresar.grid(row=0, column=0, padx=5, pady =5, ipadx=5, ipady=5)
                #boton para desplegar datos
                boton_select= ttk.Button(framebotones,text="Desplegar Tabla", command=ver, state='enabled') 
                boton_select.grid(row=0,column=1,padx=5, pady =5, ipadx=5, ipady=5)
                ttk.Button(framebotones,text="Aplicar DME" ,command=ver_dme2, state='enabled').grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)
                #boton ver grafica
                boton_grafica = ttk.Button(framebotones, text="Ver gráfica", command=ver_grafica, state='enabled')
                boton_grafica.grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
                for widget in frametodo.winfo_children():
                    widget.destroy()
            
                for widget in selectframe.winfo_children():
                    widget.destroy()
            
                for widget in my_frame_grid.winfo_children():
                    widget.destroy()
                
           
                self.show_dme.destroy()

            ttk.Button(self.show_dme,text="Volver", command=borrar).pack(padx=5, pady =5, ipadx=5, ipady=5)
            tk.Label(self.show_dme, text="Descomposición Modal Empírica",font=("Arial", 20)).pack(padx=5,   pady =5, ipadx=5, ipady=5)
            def on_exit():
                messagebox.showerror("Error", "Para salir de clic al botón volver", parent=self.show_dme)

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
            funcion= tk.StringVar(selectframe)
            funcion.set("Seleccione la Descomposición")

            opciones = []
            for line in range(len(IMFS)):
                opciones.append(line)
                #print (line)            
            global dropselect
            dropselect = ttk.OptionMenu(selectframe, funcion, *opciones)
            dropselect.pack(padx=5, pady =5, ipadx=5, ipady=5)
            
            def ver_dme():
                global seleccion
                seleccion= funcion.get()
                if(seleccion=="Seleccione la Descomposición"):
                    messagebox.showerror("Error", "Selecciona una DME para visualizar", parent=self.show_dme)
                else:
                    for widget in frametodo.winfo_children():
                        widget.destroy()
                    global my_canvas           
                    a.clear()        
                    a.plot(IMFS[int(seleccion)])
                    a.legend(["IMF "+str(seleccion)])
                    a.set_title("DME "+str(seleccion))
                    a.set_xlabel("Tiempo [s]")
                    canvas2 = FigureCanvasTkAgg(f, frametodo)
                    canvas2.show()
                    canvas2.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                    toolbar = NavigationToolbar2TkAgg(canvas2,frametodo)
                    toolbar.update()
                    toolbar.pack()
                    my_canvas = canvas2


            def prueba():
                seleccion= funcion.get()
                if (seleccion == "Seleccione la Descomposición"):
                    messagebox.showerror("Error", "Selecciona una DME para visualizar", parent=self.show_dme)
                else:
                    for widget in frametodo.winfo_children():
                        widget.destroy()
                    file_name = os.path.basename(path)
                    index_of_dot = file_name.index('.')
                    file_name_without_extension = file_name[:index_of_dot]
                    #print (file_name_without_extension)
                    global mycanvas3
                  
                   
                    a.clear()
                    a.plot(my_graph)
                    a.plot(IMFS[int(seleccion)])
                    a.legend(["Datos "+lista[0],"IMF "+str(seleccion)])
                    a.set_title(file_name_without_extension + " y " + "DME "+str(seleccion) )
                    canvas3 = FigureCanvasTkAgg(f, frametodo)
                    canvas3.show()
                    canvas3.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                    toolbar = NavigationToolbar2TkAgg(canvas3,frametodo)
                    toolbar.update()
                    toolbar.pack()
                    #canvas3._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
                    mycanvas3 = canvas3


            def guardar():
                
                my_dme= funcion.get()
                if (my_dme == "Seleccione la Descomposición"):
                    messagebox.showerror("Error", "Selecciona una DME para guardar", parent=self.show_dme)
                else:
                    for widget in frametodo.winfo_children():
                        widget.destroy()
                    messagebox.showinfo("Correcto", "Archivo Guardado con exito", parent=self.show_dme)
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
            ttk.Button(my_frame_grid, text="Desplegar grafica", command=ver_dme).grid(row=0, column=0,padx=5, pady =5, ipadx=5, ipady=5)
            ttk.Button(my_frame_grid, text="Comparacion con los datos", command=prueba).grid(row=0, column=2,padx=5, pady =5, ipadx=5, ipady=5)
            ttk.Button(my_frame_grid, text="Guardar DME", command=guardar).grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)
            frametodo.pack()

          
        

        ttk.Button(framebotones,text="Aplicar DME" ,command=ver_dme2).grid(row=0, column=3,padx=5, pady =5, ipadx=5, ipady=5)


    


   

app= AnalisisClima()
app.mainloop()

