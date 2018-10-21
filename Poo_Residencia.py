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

        for F in (Inicio, Show_dialog, Show_data, Show_graph):

        
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
        volver.grid(row=0, column=0, padx=15, pady =5, ipadx=5, ipady=5)
        label = tk.Label(self, text="Seleccionar Archivo", font=("Arial", 20))
        label.grid(row=0, column=1)

        def opendialog():
            #ruta.filename=filedialog.askdirectory()
            filename=filedialog.askopenfilename(title='Seleccionar el archivo de informacion', filetypes=(("Archivos Data","*.dat"),("Todos los Archivos","*.*")))   
            messagebox.showinfo("Archivo Seleccionado", filename)
            global path
            path=filename
            ver_data=ttk.Button(self, text="Ver Archivo", command=lambda:controller.show_frame(Show_data))
            ver_data.grid(row=2, column=1, padx=5, pady =5, ipadx=5, ipady=5)
           
            
        
        
        boton_select= ttk.Button(self,text="Abrir Archivo", command=opendialog) 
        boton_select.grid(row=1, column=1, padx=5, pady =5, ipadx=5, ipady=5)
       




#ventana para ver los datos
class Show_data(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        def ver():

            array1year=[]
            array1month=[]
            array2=[]
            #limpieza de datos
            for line in open(path):
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
            global my_graph
            my_graph = df["valor"].astype(float)
        
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

            #boton ver grafica
            boton_grafica = ttk.Button(self, text="Ver grafica", command=lambda:controller.show_frame(Show_graph))
            boton_grafica.pack(padx=5, pady =5, ipadx=5, ipady=5)   
        

        head=tk.Label(self,text="Visualizacion de los datos", font=("Arial", 20))
        head.pack()
        boton_select= ttk.Button(self,text="Desplegar Tabla", command=ver) 
        boton_select.pack(padx=5, pady =5, ipadx=5, ipady=5)
        


class Show_graph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def ver_grafica():
            a.plot(my_graph)
            a.set_title("ONI")
            a.set_xlabel("Años")
            a.set_ylabel("Datos ONI")
            a.set_xticks([0,100,200,300,400,500,600], [1996,1970,1980,1990,2000,2015,2017])
            a.set_xticklabels([0,1996,1970,1980,1990,2000,2015,2017])
            
            canvas = FigureCanvasTkAgg(f, self)
            canvas.show()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

            ttk.Button(self,text="Aplicar EMD").pack(padx=5, pady =5, ipadx=5, ipady=5)
        
        tk.Label(self, text="Grafica", font=("Arial",20)).pack()
        ttk.Button(self,text="Desplegar grafica", command=ver_grafica).pack(padx=5, pady =5, ipadx=5, ipady=5)


class Show_emd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)     


app= AnalisisClima()
app.mainloop()

