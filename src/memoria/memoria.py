import sqlite3
from config import DB_PATH

class MemoriaConversacion:
    
    def __init__(self, limit = 10 ):
        self.historial = []
        self.limit = limit
        
        self.cargar_historial()
        
    def add_user(self, message):
        self.historial.append({
            "role":"user",
            "content":message
        })
        self.guardar_sqlite(
            "user",
            message
        )
        self._limitar()
        
    def add_assistant(self, message):
        self.historial.append({
            "role":"assistant",
            "content":message
        })
        self.guardar_sqlite(
            "assistant",
            message
        )
        self._limitar()
        
    def get_context(self):
        context = ""
        for message in self.historial:
            rol = message["role"]
            content = message["content"]
            context += (
                f"{rol}: {content}\n"
            )
        return context
    
    def _limitar(self):
        if len(self.historial) > self.limit:
            self.historial = (
                self.historial[-self.limit:]
            )
            
    def guardar_sqlite(self, rol, mensaje):

        conexion = sqlite3.connect(DB_PATH)

        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO conversaciones
        (rol, mensaje)
        VALUES (?, ?)
        """,
        (rol, mensaje))

        conexion.commit()
        conexion.close()
            
    def cargar_historial(self):

        conexion = sqlite3.connect(DB_PATH)

        cursor = conexion.cursor()

        cursor.execute("""
        SELECT rol, mensaje
        FROM conversaciones
        ORDER BY id DESC
        LIMIT ?
        """,
        (self.limit,)
        )

        filas = cursor.fetchall()

        conexion.close()

        self.historial = []

        for rol, mensaje in reversed(filas):

            self.historial.append({
                "role": rol,
                "content": mensaje
            })
        