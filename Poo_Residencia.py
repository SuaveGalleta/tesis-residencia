import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 


#global ruta_new

class AnalisisClima(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Asignación del titulo de la ventana principal
        self.title("Analisis de Datos Climaticos")
        
            
        """
        #Creacion del menu
        menubar = tk.Menu(container)
        tk.Tk.config(self, menu=menubar)
        #Asigando las diferentes opciones del menu
        filemenu= tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open File...", command=lambda:me.opendialog())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        
        view= tk.Menu(menubar, tearoff=0)
        view.add_command(label="Show Data", command=lambda:self.show_frame(Show_data))
        view.add_command(label="Show Graph")
        view.add_separator()
        view.add_command(label="EMD")


        ayuda = tk.Menu(menubar, tearoff=0)
        ayuda.add_command(label="Dodumentation")
        ayuda.add_command(label="About")

        #Mostrar en la ventana el menu
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="View", menu=view)
        menubar.add_cascade(label="Help", menu=ayuda)
        """

        
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
        maintitle=tk.Label(self, text="Analisis de datos climaticos", font=("Arial",25))
        maintitle.pack(pady=10, padx=10,ipady=5, ipadx=5)
        boton_iniciar= tk.Button(self, text="Iniciar",width=20, command=lambda:controller.show_frame(Show_dialog))
        boton_iniciar.pack(padx=5, pady =5, ipadx=5, ipady=5)
        boton_salir =tk.Button(self, text="Salir", command=self.quit, width=20)
        boton_salir.pack(padx=5, pady =5, ipadx=5, ipady=5)


class Show_dialog(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        volver= tk.Button(self, text="Volver", command=lambda:controller.show_frame(Inicio))
        volver.grid(row=0, column=0, padx=15, pady =5, ipadx=5, ipady=5)
        label = tk.Label(self, text="Seleccionar Archivo", font=("Arial", 20))
        label.grid(row=0, column=1)

        def opendialog():
            #ruta.filename=filedialog.askdirectory()
            self.filename=filedialog.askopenfilename(title='Seleccionar el archivo de informacion', filetypes=(("Archivos Data","*.dat"),("Todos los Archivos","*.*")))   
            messagebox.showinfo("Archivo Seleccionado", self.filename)
            ver_data=tk.Button(self, text="Ver Archivo", command=lambda:controller.show_frame(Show_data))
            ver_data.grid(row=2, column=1, padx=5, pady =5, ipadx=5, ipady=5)
            return self.filename
        
        
        boton_select= tk.Button(self,text="Abrir Archivo", command=opendialog) 
        boton_select.grid(row=1, column=1, padx=5, pady =5, ipadx=5, ipady=5)
       


class Show_data(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def ver():
            messagebox.showinfo("Archivo Seleccionado", )

        boton_select= tk.Button(self,text="Abrir Archivo", command=ver) 
        boton_select.grid(row=1, column=1, padx=5, pady =5, ipadx=5, ipady=5)
        
        



  
        
        
        

        


app= AnalisisClima()
app.mainloop()

