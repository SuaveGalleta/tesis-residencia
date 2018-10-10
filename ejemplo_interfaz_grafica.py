from tkinter import *

root = Tk()

root.title("Hola mundo")
root.resizable(1,1)
root.iconbitmap("logo_tec.ico")

frame = Frame(root, width=480, height=320)
frame.pack()

label =  Label()
Label( frame, text="hola mundo").place(x =0, y = 0)
#frame.config(cursor="pirate")
#frame.config(bg="lightblue" )
#frame.config(bd=25)
#frame.config(relief="sunken")

#root.config(cursor="arrow")
#root.config(bg="blue" )
#root.config(bd=15)
#root.config(relief="ridge")





#abajo del todo
root.mainloop()