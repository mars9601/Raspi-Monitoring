"""
    Ausgangsbeschreibung:   "Programm zum Auslesen der CPU- und RAM-
                            Auslastung und Export in das CSV-Datenformat."

    Autor:                  K. Faengmer
    Datum:                  09.12.2020

    Aktuelle Beschreibung:  "Programm zum Auslesen der CPU- und RAM-
                            Auslastung und senden dieser an eine
                            Datenbank, sowie zuum Abrufen einer Statistik
                            der minimalen, maximalen und durschnittlichen
                            Auslastung der letzten zwei Stunden. 

    Überarbeitet durch:     Kyra Werner, Richard Voth, Mia Möbes (06.03.2021)
    Überarbeitet durch:     K. Faengmer (08.09.2021)
"""


import rp
import psutil
import mysql.connector
from datetime import datetime

while True:

    print("")
    print("")
    print("")
    print("")
    print("")

    # Benutzermenu
    print("==============================")
    print("   RASPBERRY PI MONITORING    ")
    print("==============================")
    print(" [1] Daten aufzeichnen        ")
    print(" [2] Statistik ausgeben       ")
    print(" [3] Geräte anzeigen          ")
    print("------------------------------")
    print(" [0] Programm beenden         ")
    print("==============================")
    
    antwort = input("Wählen Sie [0-3]: ")


        
    # Programm beenden
    if( antwort == "0"):
        print("Das Programm wird nun beendet...")
        break

    # Datenbankverbindung aufbauen
    if( antwort == "1" or antwort == "2" or antwort == "3"):
        rpidb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="raspi")
        
        mycursor = rpidb.cursor()
        
        print("")
        print("")
        print("")
        print("")
        print("")

    if(antwort == "1"):

        print("==============================")
        print("      DATEN AUFZEICHNEN       ")
        print("==============================")
        table = input("Gerät angeben: ")
        print("")
        
        #Kopfzeile der Bildschirmausgabe
        print("ZEITSTEMPEL \t\t CPU [%]\t RAM [%]")
        
        try:
            while True:            
                # Zeit und Auslastung ermitteln
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cpu = psutil.cpu_percent(1)
                ram = psutil.virtual_memory().percent

                # Bildschirmausgabe und Datenbankeingabe
                print(time,"\t",cpu,"\t",ram)
                rp.insertInto(time, cpu, ram, mycursor, rpidb, table)

        # Beenden des Vorgangs und Abbau der Datenbankverbindung1
        

        except KeyboardInterrupt:
            print("... Abbruch!")
            rpidb.close()

    elif(antwort == "2"):
        
    

        # Statistik aufrufen
        print("==============================")
        print("   STATISTIK ZUR AUSLASTUNG   ")
        print("==============================")
        table = input("Gerät angeben: ")
        print("")
        
        # Daten für Statistik abrufen
        maxCpu = rp.statsMaxCPU(mycursor, table)
        avgCpu = rp.statsAvgCPU(mycursor, table)
        minCpu = rp.statsMinCPU(mycursor, table)
        maxRam = rp.statsMaxRAM(mycursor, table)
        avgRam = rp.statsAvgRAM(mycursor, table)
        minRam = rp.statsMinRAM(mycursor, table)
        
        print("\t CPU \t RAM")
        print("MIN.\t " + str('{:.1f}'.format(minCpu[0])) + "\t " + str('{:.1f}'.format(minRam[0])))
        print("MAX.\t " + str('{:.1f}'.format(maxCpu[0])) + "\t " + str('{:.1f}'.format(maxRam[0])))
        print("AVG.\t " + str('{:.1f}'.format(avgCpu[0])) + "\t " + str('{:.1f}'.format(avgRam[0])))
        
        # Datenbankverbindung trennen
        rpidb.close()

    elif(antwort == "3"):
        
        print("==============================")
        print("     REGISTRIERTE GERÄTE      ")
        print("==============================")
        
        for table_name in rp.showTables(mycursor):
           print('Gerätenamen: {}'.format(*table_name))
        
        
    else:
        print("")
