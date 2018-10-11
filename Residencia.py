import tkinter as tk 

class main(tk.Tk):

    def __init__(self, *args, **kwargs):

        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        

        container.pack(side="top",fill="both", expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        frame = Startpage(container, self)
        self.frames[Startpage] = frame
        frame.grid(row=0, column = 0, sticky="nsew")
        self.show_frame(Startpage)
    
    def show_frame(self,count):
        frame = self.frames[count]
        frame.tkraise()

class Startpage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        etiquetatitulo = tk.Label(self, text= "Bienvenidos")
        etiquetatitulo.pack(pady=10, padx=10)

app=main()
app.title("Analisis de datos climaticos")
app.geometry("600x350") 
app.iconbitmap("logo_tec.ico")
app.mainloop()




"""


root = Tk()

root.title("Analisis de datos climaticos")
root.resizable(1,1)
root.geometry("600x350")
root.iconbitmap("logo_tec.ico")

#Menu

menubar = Menu(root)
root.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Abrir Archivo")
filemenu.add_separator()
filemenu.add_command(label="Cerrar")

analisismenu = Menu(menubar, tearoff=0)
analisismenu.add_command(label="EMD")

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Ayuda")
helpmenu.add_separator()
helpmenu.add_command(label="Acerca de...")

menubar.add_cascade(label="Archivo", menu = filemenu)
menubar.add_cascade(label="Analisis", menu = analisismenu)
menubar.add_cascade(label="Ayuda", menu = helpmenu)



# ventana Inicio
frame = Frame(root, width = 250, height = 250)
frame.pack(fill = "both", expand = 1)
path = PhotoImage(file = "logo_tec.png")
logo = Label(frame, image= path, width= 100, height=100)
logo.pack(pady = 5,ipady=5)
etiquetatitulo = Label(frame, text= "Bienvenidos")
etiquetatitulo.config(font=("Arial", 25))
etiquetatitulo.pack(pady = 5,ipady=5)
etiquetatitulo2 = Label(frame, text="Sistema para el analisis de datos climaticos")
etiquetatitulo2.config(font=("Arial", 20))
etiquetatitulo2.pack(padx=5, pady = 5, ipadx=5,ipady=5)
Button(frame, text="Iniciar", width=20).pack(padx=5, pady =10)
Button(frame, text="Salir", width=20).pack(padx=5, pady =10)
"""










