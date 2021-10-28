# Daten in Datenbank einfügen
def insertInto(time, cpu, ram, cursor, database, table):
    sql = "INSERT INTO " + table + "(Timestamp, CPU, RAM) VALUES(%s, %s, %s)"
    val = (time, cpu, ram)
    cursor.execute(sql, val)
    database.commit()

# Gerätenamen anzeigen
def showTables(cursor):
    sql = "SHOW TABLES"
    cursor.execute(sql)
    return cursor.fetchall()  

# MIN. CPU-Auslastung in letzten 2 Stunden ermitteln
def statsMinCPU(cursor, table):
    sql = "SELECT MIN(CPU) FROM " + table +" WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
    cursor.execute(sql)
    return cursor.fetchone()
    
# MAX. CPU-Auslastung in letzten 2 Stunden ermitteln
def statsMaxCPU(cursor, table):
    sql = "SELECT MAX(CPU) FROM "+table+" WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
    cursor.execute(sql)
    return cursor.fetchone()
    
# AVG. CPU-Auslastung in letzten 2 Stunden ermitteln
def statsAvgCPU(cursor, table):
    sql = "SELECT AVG(CPU) FROM " + table +" WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
    cursor.execute(sql)
    return cursor.fetchone()

# MIN. RAM-Auslastung in letzten 2 Stunden ermitteln
def statsMinRAM(cursor, table):
    sql = "SELECT Min(RAM) FROM "+ table +" WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
    cursor.execute(sql)
    return cursor.fetchone()
    
# MAX. RAM-Auslastung in letzten 2 Stunden ermitteln
def statsMaxRAM(cursor, table):
    sql = "SELECT MAX(RAM) FROM "+ table +" WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
    cursor.execute(sql)
    return cursor.fetchone()

# AVG. RAM-Auslastung in letzten 2 Stunden ermitteln
def statsAvgRAM(cursor, table):
    sql = "SELECT AVG(RAM) FROM "+ table +" WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
    cursor.execute(sql)
    return cursor.fetchone()



