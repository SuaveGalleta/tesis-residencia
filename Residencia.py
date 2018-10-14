"""
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
        path = tk.PhotoImage(file = "logo_tec.png")
        logo = tk.Label(self, image= path)
        logo.pack(pady = 5,ipady=5)      
        etiquetatitulo = tk.Label(self, text= "Bienvenidos")
        etiquetatitulo.config(font=("Arial", 25))
        etiquetatitulo.pack(pady=10, padx=10)
        etiquetatitulo2 = tk.Label(self, text="Sistema para el analisis de datos climaticos")
        etiquetatitulo2.config(font=("Arial", 20))
        etiquetatitulo2.pack(padx=5, pady = 5, ipadx=5,ipady=5)
        tk.Button(self, text="Iniciar", width=20).pack(padx=5, pady =10)
        tk.Button(self, text="Salir", width=20).pack(padx=5, pady =10)

app=main()
app.title("Analisis de datos climaticos")
app.geometry("600x350") 
app.iconbitmap("logo_tec.ico")
app.mainloop()




"""

from tkinter import *
root = Tk()

root.title("Analisis de datos climaticos")
root.resizable(1,1)
root.geometry("600x350")
root.iconbitmap("logo_tec.ico")

#comandos para los botones

#comando para salir
def salir():
    root.quit()

#comando abrir nueva ventana
def cargar_archivos():
    #ventana de la seleccion de datos climaticos
    abrir_data=Tk()
    abrir_data.title("Analisis de datos climaticos")
    abrir_data.resizable(1,1)
    abrir_data.geometry("600x350")
    abrir_data.iconbitmap("logo_tec.ico")
    frame2 = Frame(abrir_data, width=250, height=250)
    frame2.grid(row=0, colum=1)
    frame3 = Frame(abrir_data, width=250, height=250)
    frame3.grid(row=0, colum=2)
    titulo2=Label(frame2, text="Seleccione el archivo" )
    titulo2.config(font=("Arial", 15))

    titulo2.grid(padx=5, pady =5, row=0, column=3)
    direccion = Entry(frame2, width=40)
    direccion.config()
    direccion.grid(padx=5, pady=5, ipadx=5, ipady=5, row=1, column=3 ) 
    file_choosser= Button(frame2, text="Seleccionar Archivo" ,width=20)
    file_choosser.config()
    file_choosser.grid(padx=5, pady=5, ipadx=5, ipady=5, row=1, column=4, side="center")
    root.iconify()
















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
Button(frame, text="Iniciar", width=20, command=cargar_archivos).pack(padx=5, pady =10)
Button(frame, text="Salir", width=20, command=salir).pack(padx=5, pady =10)




root.mainloop()









