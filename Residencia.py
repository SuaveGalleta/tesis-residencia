from tkinter import *


root = Tk()

root.title("Analisis de datos climaticos")
root.resizable(1,1)
root.geometry("600x350")
root.iconbitmap("logo_tec.ico")

#Menu
"""
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
"""


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











root.mainloop()