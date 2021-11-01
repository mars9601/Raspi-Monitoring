"""
Beschreibung:
Programm zum Auslesen und zur graphischen Visualisierung von CPU- und RAM Daten, welche in einer Datenbank gespeichert sind.
Es werden  live CPU- und RAM-Daten, sowie 24h-Statistiken über die minimale, maximale und durschnittliche Auslastung dargestellt.
Die Daten und ihre zugehörigen Graphen werden jede Sekunde erneuert.

Autoren: David Bongard, Fabian Pütz, Niklas Papageorgiou

Zuletzt bearbeitet: 22.10.2021

Notiz:
connect Funktion muss bei jedem refresh aufgerufen werden, da das Programm sonst nicht die neusten Live-Daten bekommt.
"""

import tkinter as tk
from tkinter import Frame, ttk
from tkinter import messagebox
from tkinter.constants import EW
from typing import Text
import mysql.connector
from datetime import datetime
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import time

# pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --user matplotlib


# Globale Variable speichert Datenbank nach erfolgreicher Verbindung
# Für Nutzung DB außerhalb connect Funktion
db = None

# globale error-Zähler verhindern error-loop beim plot refresh
noval_err1 = 0
noval_err2 = 0

# connect-Funktion stellt Verbindung zur DB her
# Bei connect-Problemen -> ERROR
def connect(dbhost, dbname, username, passwd, dev):
    global db
    #connect nur wenn DB nich manuell disconnected wurde --> nötig wegen automatischer Wiederholung der connect Funktion
    try:
        print(db)
        if db != "disconnected":
            # connect nur wenn Gerät angegeben
            if dev != "":
                db = mysql.connector.connect(
                host = dbhost,                                                                         
                user = username,
                password = passwd,
                database = dbname
                )

                if checktable(dev) != True:
                    err_device = "Gerät " + dev + " existiert nicht!"
                    messagebox.showerror("DEVICE NOT FOUND!",message=err_device)
                else:
                    # Connect button wird deaktiviert
                    con_button["state"] = "disabled"
                    dbstats(dev)
                    livestats(dev)
                    # Wiederholung der connect Funktion nötig für neue Werte und refresh der Graphen
                    con_button.after(1000,lambda: connect(entry1.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get()))
            else:
                dev_info = "Bitte gib ein Gerät an!"
                messagebox.showinfo("NO DEVICE SELECTED",message=dev_info)
        
        # db zurücksetzen auf Standardwert ermöglicht erneutes manuelles verbinden
        else:
            db = None
    
    except:
        msg_err = "Verbindung zu " + dbname + " konnte nicht hergestellt werden!"
        messagebox.showerror("NO CONNECT ERROR",message=msg_err)

# kappt die Datenbankverbindung 
def disconnect():
    global db
    if db != None and db != "disconnected":
        msg = "Verbindung zur Datenbank getrennt!"
        messagebox.showinfo("Disconnect successful",message=msg)
        db.close()
        db = "disconnected"
        # Connect Button wird reaktiviert
        con_button["state"] = "normal"

def checktable(table):
    global db
    mycursor = db.cursor()
    mycursor.execute("SHOW TABLES LIKE '%s'"% (table))

    for x in mycursor:                                      
        if table in x:
            return True
        else:
            return False

# 24h-Statistik
def dbstats(dev):
    global noval_err1
    mycursor = db.cursor()                                                                                    

# MIN,MAX und AVG CPU und RAM Daten der letzten 24h werden aus DB ausgelesen und gespeichert
# Kein try-except nötig, da kein Fehler. Es wird als Wert "None" gespeichert
    mycursor.execute("SELECT MIN(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dev))
    min_cpu = mycursor.fetchone()[0]
    mycursor.execute("SELECT MIN(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dev))
    min_ram = mycursor.fetchone()[0]
    mycursor.execute("SELECT MAX(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dev))
    max_cpu = mycursor.fetchone()[0]
    mycursor.execute("SELECT MAX(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dev))
    max_ram = mycursor.fetchone()[0]
    mycursor.execute("SELECT AVG(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dev))
    avg_cpu = mycursor.fetchone()[0]
    mycursor.execute("SELECT AVG(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);"% (dev))
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
        ax1.bar("MIN CPU",min_cpu)
        ax1.bar("MIN RAM",min_ram)
    except:
        ax1.bar("MIN CPU",0)
        ax1.bar("MIN RAM",0)
        # Wenn error bereits geworfen --> pass
        if noval_err1 > 0:
            pass
        else:
            err_noval = "Es stehen keine Daten der letzten 24h zur Verfügung!"
            messagebox.showerror("NO VALUES",message=err_noval)
            noval_err1 = 1
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
def livestats(dev):                                                                                   
    global noval_err2
# Die neusten (max. 30 Sekunde alten) Daten werden aus der Datenbank ausgelesen, falls vorhanden
# try-except hier nötig, da dieser SQL-Befehl Fehler wirft wenn keine Daten (da nichts übergeben wird)
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT CPU FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 0.5 MINUTE) ORDER BY Timestamp DESC LIMIT 1;"% (dev))
        live_cpu = mycursor.fetchone()[0]
        mycursor.execute("SELECT RAM FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 0.5 MINUTE) ORDER BY Timestamp DESC LIMIT 1;"% (dev))
        live_ram = mycursor.fetchone()[0]
        mycursor.close()
    except:
        # Wenn error bereits geworfen --> pass
        if noval_err2 > 0:
            pass
        else:
            err_noval = "Für dieses Gerät sind keine Live-Daten verfügbar!"
            messagebox.showerror("NO VALUES",message=err_noval)
            noval_err2 = 1

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
root = tk.Tk()
root.geometry('890x626')
root.title("Hardware Monitoring")
root.columnconfigure((0,1, 2),  weight=1)

# Überschrift
label1 = tk.Label(root,font= "14",fg="white",bg="grey",text= "Willkommen beim Raspi Monitoring")
label1.grid(row=0, columnspan=3, sticky=tk.EW, ipady=20)

# Label und Eingabefelder werden erstellt, gesetzt und positioniert
dbserver_label = tk.Label(root, text= "Datenbankserver:")
dbserver_label.grid(row=1, column=0, sticky=tk.W, ipady= 10, ipadx= 10)
entry1 = ttk.Entry(root)
entry1.grid(row=1, column=0,sticky=tk.E, ipady= 5)

dbname_label = tk.Label(root,text= "Datenbankname: ")
dbname_label.grid(row=2, column=0, sticky=tk.W, ipady= 10, ipadx= 10)
entry2 = ttk.Entry(root)
entry2.grid(row=2, column=0,sticky=tk.E, ipady= 5)

dbuser_label = tk.Label(root, text= "Benutzer: ")
dbuser_label.grid(row=1, column=1,sticky=tk.W, ipady= 10, ipadx= 10)
entry3 = ttk.Entry(root)
entry3.grid(row=1, column=1,sticky=tk.E, ipady= 5)

db_pw_label = tk.Label(root, text= "Passwort: ")
db_pw_label.grid(row=2, column=1,sticky=tk.W, ipady= 10, ipadx= 10)
entry4 = ttk.Entry(root)
entry4.grid(row=2, column=1,sticky=tk.E, ipady= 5)

db_table_label = tk.Label(root, text= "Gerät:")
db_table_label.grid(row=3, column=0, sticky=tk.W, ipady= 10, ipadx= 10)
entry5 = ttk.Entry(root)
entry5.grid(row=3, column=0,sticky=tk.E, ipady= 5)

# Verbinden, Trennen und Beenden Button
# Buttons werden erstellt, postitioniert und mit Funktionen bestückt
# Umweg über lambda Funktion erlaubt Übergabe von Parametern
con_button= tk.Button(root,text= "Verbinden", bg="lightgreen", command= lambda: connect(entry1.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get()))
con_button.grid(row=1, column=2, sticky=tk.NS, pady=5)

discon_button= tk.Button(root,text= "Trennen", bg="orange", command= disconnect)
discon_button.grid(row=2, column=2, sticky=tk.NS, ipadx=5, pady=5)

close_button=tk.Button(root,text="Beenden", bg="red", command=root.quit)
close_button.grid(row=3, column=2, sticky=tk.NS, ipadx=3, pady=5)

# Live-Anzeige und 24h Statistik Ausgabe
notebook = ttk.Notebook(root)
notebook.grid(row=6, columnspan=5)

# Reiter des Notebooks
tab1 = Frame(notebook, width=800, height=400)
tab2 = Frame(notebook, width=800, height=400)
notebook.add(tab1, text="Live Anzeige")
notebook.add(tab2, text="24h Statistik" )

# Macht Fenster-Größe und Widget-Positionen flexibel
root.resizable(True, True)

# Endd-Funktion der GUI
root.mainloop()
