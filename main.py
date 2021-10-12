from datetime import datetime
from logging import root
import tkinter  
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from tkinter.messagebox import askyesno
import mysql.connector
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import psutil
import matplotlib.animation as animation

#test




root = tkinter.Tk()
root.resizable(width=1,height=1)
root.title("Auslastung")
Label(root, text="Datenbankserver").grid(row=0, column=0, padx=10, pady=10)
Label(root, text="Datenbankname").grid(row=1, column=0, padx=10, pady=10)
Label(root, text="Benutzer").grid(row=0, column=2, padx=10, pady=10)
Label(root, text="Password").grid(row=1, column=2, padx=10, pady=10)

e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root)
e4 = Entry(root)

e1.grid(row=0, column=1, padx=10, pady=10)
e2.grid(row=1, column=1, padx=10, pady=10)
e3.grid(row=0, column=3, padx=10, pady=10)
e4.grid(row=1, column=3, padx=10, pady=10)



time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu = psutil.cpu_percent(1)
ram = psutil.virtual_memory().percent

print(time,"\t",cpu,"\t",ram)



"""
fig1, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(x, y)
ax2.plot(x, -y)
ax1.set_title("RAM")
ax2.set_title("CPU")   
"""




fig1 = plt.figure()
gs1 = fig1.add_gridspec(1, 2, wspace=0)
axs1 = gs1.subplots(sharex=True, sharey=True)
axs1[0].plot(time, cpu)
axs1[1].plot(ram,0)
axs1[0].set_title("RAM")
axs1[1].set_title("CPU")











def kill():
    answer = askyesno(title='Beenden ?',message='Wollen Sie das Programm wirklich beenden ?')
    if answer:
        root.destroy()



Button(root, text="Login",width=10,height=1).grid(row=0, column=4, padx=10, pady=10)
Button(root, text="Beenden",width=10,height=1, command=kill).grid(row=1, column=4, padx=10, pady=10)


my_notebook = ttk.Notebook(root)
my_notebook.grid(row=6, columnspan=5)

canvas = FigureCanvasTkAgg(fig1, master=root)
canvas.draw() 



my_frame1 = canvas.get_tk_widget()
my_frame2 = Frame(my_notebook, width=700, height=300, bg="red")



my_notebook.add(my_frame1,text="Live-Anzeige")
my_notebook.add(my_frame2,text="24-h")

root.mainloop()
