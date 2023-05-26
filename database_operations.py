import psycopg2
from datetime import datetime

from emergency import Emergency

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="central_116_database",
        user="postgres",
        password="postgres"
    )
    return conn

def store_snapshot_data(snapshot_data):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    snapshot = snapshot_data.decode()
    url = "http://example.com"
    origin = "example.com"
    
    cursor.execute(
        "INSERT INTO snapshots (datetime, snapshot, url, origin) VALUES (%s, %s, %s, %s)",
        (timestamp, snapshot, url, origin)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_pending_gps():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT identifier FROM emergencies WHERE gps = '0'")
    rows = cursor.fetchall()
    cursor.close()
    return [row[0] for row in rows]

def insert_emergencies(emergencies):
    conn = get_connection()
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS emergencies
                 (identifier TEXT PRIMARY KEY, timestamp TEXT, location TEXT, type TEXT, status TEXT, units TEXT, other TEXT, map TEXT, gps TEXT)''')

    # Crear la tabla history si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS history
                 (text TEXT, timestamp TEXT)''')

    # Insertar o actualizar cada emergency en la tabla
    for emergency in emergencies:
        # Verificar si el identificador ya existe en la tabla
        cursor.execute("SELECT * FROM emergencies WHERE identifier = %s", (emergency.identifier,))
        result = cursor.fetchone()

        if result is None:
            # Si el identificador no existe, insertar el registro
            cursor.execute("INSERT INTO emergencies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0)",
                      (emergency.identifier, emergency.timestamp, emergency.location, emergency.type, emergency.status, emergency.units, emergency.other, emergency.map))
            print(f"New emergency created with identifier {emergency.identifier}")
            add_to_history(conn, f"New emergency created with identifier {emergency.identifier}")
        else:
            # Si el identificador ya existe, actualizar los campos que hayan cambiado
            old_emergency = Emergency(*result)
            new_emergency = emergency

            if old_emergency.units != new_emergency.units:
                print(f"Units changed from {old_emergency.units} to {new_emergency.units}")
                add_to_history(conn, f"Units changed from {old_emergency.units} to {new_emergency.units}")
            if old_emergency.status != new_emergency.status:
                print(f"Status changed from {old_emergency.status} to {new_emergency.status}")
                add_to_history(conn, f"Status changed from {old_emergency.status} to {new_emergency.status}")
            if old_emergency.type != new_emergency.type:
                print(f"Type changed from {old_emergency.type} to {new_emergency.type}")
                add_to_history(conn, f"Type changed from {old_emergency.type} to {new_emergency.type}")
            if old_emergency.location != new_emergency.location:
                print(f"Location changed from {old_emergency.location} to {new_emergency.location}")
                add_to_history(conn, f"Location changed from {old_emergency.location} to {new_emergency.location}")
            if old_emergency.other != new_emergency.other:
                print(f"Other changed from {old_emergency.other} to {new_emergency.other}")
                add_to_history(conn, f"Other changed from {old_emergency.other} to {new_emergency.other}")

            cursor.execute("UPDATE emergencies SET timestamp = %s, location = %s, type = %s, status = %s, units = %s, other = %s, map = %s WHERE identifier = %s",
                      (new_emergency.timestamp, new_emergency.location, new_emergency.type, new_emergency.status, new_emergency.units, new_emergency.other, new_emergency.map, new_emergency.identifier))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    cursor.close()
    conn.close()

def add_to_history(conn, text):
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO history VALUES (%s, %s)", (text, timestamp))
    conn.commit()
    cursor.close()