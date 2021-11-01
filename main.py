from datetime import datetime
import tkinter  
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter.messagebox import askyesno
from tkinter import messagebox
import mysql.connector
from mysql.connector.errors import Error
import time




db= None

errorcheck1 = 0
errorcheck2 = 0


def connect(dbhost, dbname, dbuser, dppass, dbdev):
    global db
    #connect nur wenn DB nich manuell getrennt wurde --> nötig wegen automatischer Wiederholung der connect Funktion
    try:
        print(db)
        if db != "getrennt":
            # connect nur wenn Gerät angegeben
            if dbdev != "":
                db = mysql.connector.connect(
                host = dbhost,                                                                         
                user = dbuser,
                password = dppass,
                database = dbname
                )

                if devcheck(dbdev) != True:
                    no_dbdev = "Gerät " + dbdev + " existiert nicht!"
                    messagebox.showerror("Gerät nicht in Datenbank gefunden!",message=no_dbdev)
                else:
                    # Connect button wird deaktiviert
                    loginbtn["state"] = "disabled"
                    dblog24(dbdev)
                    dbloglive(dbdev)
                    # Wiederholung der connect Funktion nötig für neue Werte und refresh der Graphen
                    loginbtn.after(1000,lambda: connect(e1.get(),e2.get(),e4.get(),e5.get(),e3.get()))
            else:
                dbdev_info = "Bitte ein Gerät angeben!"
                messagebox.showinfo("Kein Gerät ausgewählt",message=dbdev_info)
        
        # db zurücksetzen auf Standardwert ermöglicht erneutes manuelles verbinden
        else:
            db = None
    
    except:
        msg_err = "Verbindung zu " + dbname + " konnte nicht aufgebaut werden"
        messagebox.showerror("Keine Verbindung",message=msg_err)


# kappt die Datenbankverbindung 
def disconnect():
    global db
    if db != None and db != "getrennt":
        dc = "Verbindung zur Datenbank getrennt!"
        messagebox.showinfo("Getrennt!",message=dc)
        db.close()
        db = "getrennt"
        # Connect Button wird reaktiviert
        loginbtn["state"] = "normal"

    


def devcheck(table):
    global db
    mycursor = db.cursor()
    mycursor.execute("SHOW TABLES LIKE '%s'"% (table))

    for x in mycursor:                                      
        if table in x:
            return True
        else:
            return False

# 24h-Statistik
def dblog24(dbdev):
    global errorcheck1
    mycursor = db.cursor()                                                                                    

# MIN,MAX und AVG CPU und RAM Daten der letzten 24h werden aus DB ausgelesen und gespeichert
# Kein try-except nötig, da kein Fehler. Es wird als Wert "None" gespeichert
    mycursor.execute("SELECT MIN(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dbdev))
    min_cpu = mycursor.fetchone()[0]
    mycursor.execute("SELECT MIN(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dbdev))
    min_ram = mycursor.fetchone()[0]
    mycursor.execute("SELECT MAX(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dbdev))
    max_cpu = mycursor.fetchone()[0]
    mycursor.execute("SELECT MAX(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dbdev))
    max_ram = mycursor.fetchone()[0]
    mycursor.execute("SELECT AVG(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dbdev))
    avg_cpu = mycursor.fetchone()[0]
    mycursor.execute("SELECT AVG(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dbdev))
    avg_ram = mycursor.fetchone()[0]
    mycursor.close() 
        

# Bar Plots mit DB Daten werden erstellt für MAX,MIN und AVG CPU/RAM
# try-except nötig, da plot mit Wert None nicht möglich
# Eine Fehlermeldung reicht, daher bei fig2/3 except: pass um Fehlermeldung in Konsole zu umgehen
    fig1 = plt.Figure(figsize=(3,4),dpi=100)
    ax1 = fig1.add_subplot()
    ax1.set_ylim((0,100))
    ax1.set_title("MIN CPU/RAM")
    try:
        ax1.plot("MIN CPU",min_cpu)
        ax1.plot("MIN RAM",min_ram)
    except:
        ax1.plot("MIN CPU",0)
        ax1.plot("MIN RAM",0)
        # Wenn error bereits geworfen --> pass
        if errorcheck1 > 0:
            pass
        else:
            no_value = "Es stehen keine Daten der letzten 24h zur Verfügung!"
            messagebox.showerror("Keine Werte",message=no_value)
            errorcheck1 = 1
    canvas1 = FigureCanvasTkAgg(fig1,tab2)
    canvas1.get_tk_widget().grid(row=0, column=0)




    fig2 = plt.Figure(figsize=(3,4),dpi=100)
    ax2 = fig2.add_subplot()
    ax2.set_ylim((0,100))
    ax2.set_title("MAX CPU/RAM")
    try:
        ax2.bar("MAX CPU",max_cpu)
        ax2.bar("MAX RAM",max_ram)
    except:
        ax2.bar("MAX CPU",0)
        ax2.bar("MAX RAM",0)
    canvas2 = FigureCanvasTkAgg(fig2,tab2)
    canvas2.get_tk_widget().grid(row=0, column=1)

    fig3 = plt.Figure(figsize=(3,4),dpi=100)
    ax3 = fig3.add_subplot()
    ax3.set_ylim((0,100))
    ax3.set_title("AVG CPU/RAM")
    try:
        ax3.bar("AVG CPU",avg_cpu)
        ax3.bar("AVG RAM",avg_ram)
    except:
        ax3.bar("AVG CPU",0)
        ax3.bar("AVG RAM",0)
    canvas3 = FigureCanvasTkAgg(fig3,tab2)
    canvas3.get_tk_widget().grid(row=0, column=2)


# Live-Statistik
def dbloglive(dbdev):                                                                                   
    global errorcheck2
# Die neusten (max. 30 Sekunde alten) Daten werden aus der Datenbank ausgelesen, falls vorhanden
# try-except hier nötig, da dieser SQL-Befehl Fehler wirft wenn keine Daten (da nichts übergeben wird)
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT CPU FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 0.5 MINUTE) ORDER BY Timestamp DESC LIMIT 1;"% (dbdev))
        live_cpu = mycursor.fetchone()[0]
        mycursor.execute("SELECT RAM FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 0.5 MINUTE) ORDER BY Timestamp DESC LIMIT 1;"% (dbdev))
        live_ram = mycursor.fetchone()[0]
        mycursor.close()
    except:
        # Wenn error bereits geworfen --> pass
        if errorcheck2 > 0:
            pass
        else:
            no_value = "Für dieses Gerät sind keine Live-Daten verfügbar!"
            messagebox.showerror("NO VALUES",message=no_value)
            errorcheck2 = 1

# Bar Plot mit neusten DB Daten wird erstellt
# try-except, da beim Scheitern des letzten try-excepts live_cpu und live_ram keine Werte speichern
    fig = plt.Figure(figsize=(3,4),dpi=100)
    ax = fig.add_subplot()
    ax.set_ylim((0,100))
    ax.set_title("Live Data")
    try:
        ax.bar("CPU",live_cpu)
        ax.bar("RAM",live_ram)
    except:
        ax.bar("CPU",0)
        ax.bar("RAM",0)
    canvas = FigureCanvasTkAgg(fig,tab1)
    canvas.get_tk_widget().grid(row=0, column=0)

# Hauptfenster wird erstellt
root = tkinter.Tk()
root.title("Hardware Monitoring")

# Label und Eingabefelder werden erstellt, gesetzt und positioniert

Label(root, text="Datenbankserver").grid(row=0, column=0, padx=10, pady=10)
Label(root, text="Datenbankname").grid(row=1, column=0, padx=10, pady=10)
Label(root, text="Geräte-Name" ).grid(row=2, column=0, padx=10, pady=10)
Label(root, text="Benutzer").grid(row=0, column=2, padx=10, pady=10)
Label(root, text="Password").grid(row=1, column=2, padx=10, pady=10)


e1 = Entry(root)
e1.grid(row=0, column=1, padx=10, pady=10)

e2 = Entry(root)
e2.grid(row=1, column=1, padx=10, pady=10)

e3 = Entry(root)
e3.grid(row=2, column=1, padx=10, pady=10)

e4 = Entry(root)
e4.grid(row=0, column=3, padx=10, pady=10)

e5 = Entry(root, show="*")
e5.grid(row=1, column=3, padx=10, pady=10)


# Verbinden, Trennen und Beenden Button
# Buttons werden erstellt, postitioniert und mit Funktionen bestückt
# Umweg über lambda Funktion erlaubt Übergabe von Parameternf

loginbtn = Button(root, text="Login",width=10,height=1, command= lambda: connect(e1.get(),e2.get(),e4.get(),e5.get(),e3.get()))
closebtn = Button(root, text="Beenden",width=10,height=1, command=root.quit)
discobtn = Button(root, text="Trennen",width=10,height=1, command=disconnect)

loginbtn.grid(row=0, column=4, padx=10, pady=10)
closebtn.grid(row=2, column=4, padx=10, pady=10)
discobtn.grid(row=1, column=4, padx=10, pady=10)

# Live-Anzeige und 24h Statistik Ausgabe
notebook = ttk.Notebook(root)
notebook.grid(row=6, columnspan=5)

# Reiter des Notebooks
tab1 = Frame(notebook, width=700, height=300)
tab2 = Frame(notebook, width=700, height=300)
notebook.add(tab1, text="Live Anzeige")
notebook.add(tab2, text="24h Statistik" )

# Macht Fenster-Größe und Widget-Positionen flexibel
root.resizable(height=0,width=0)

# Endd-Funktion der GUI
root.mainloop()





































'''



def trennen():
    running = False
    rpidb.close()


def kill():
    answer = askyesno(title='Beenden ?',message='Wollen Sie das Programm wirklich beenden ?')
    if answer:
        root.destroy()



root = tkinter.Tk()
root.resizable(width=0,height=0)
root.title("Auslastung")

# Erstellen und Positionieren der Label und Eingabefelder






loginbtn = Button(root, text="Login",width=10,height=1, command=connect)
closebtn = Button(root, text="Beenden",width=10,height=1, command=kill)
discobtn = Button(root, text="Trennen",width=10,height=1, command=trennen)

loginbtn.grid(row=0, column=4, padx=10, pady=10)
closebtn.grid(row=2, column=4, padx=10, pady=10)
discobtn.grid(row=1, column=4, padx=10, pady=10)







time = 0
ram = 0
cpu = 0

fig1 = plt.figure()
gs1 = fig1.add_gridspec(1, 2, wspace=0)
axs1 = gs1.subplots(sharex=True, sharey=True)
axs1[0].plot(time, cpu)
axs1[1].plot(ram,0)
axs1[0].set_title("RAM")
axs1[1].set_title("CPU")



my_notebook = ttk.Notebook(root)
my_notebook.grid(row=6, columnspan=5)

canvas = FigureCanvasTkAgg(fig1, master=root)
canvas.draw() 



my_fram = cae1nvas.get_tk_widget()
my_frame2 = Frame(my_notebook, width=700, height=300, bg="red")



my_notebook.add(my_frame1,text="Live-Anzeige")
my_notebook.add(my_frame2,text="24-h")



#Ende der GUI
root.mainloop()
'''