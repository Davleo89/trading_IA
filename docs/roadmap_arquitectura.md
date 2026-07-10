# Roadmap de Arquitectura

## Estado actual
El proyecto mantiene una arquitectura simple y explícita.  
Se prioriza la **claridad sobre la abstracción**.  

Cada módulo abre y gestiona su propia conexión SQLite con el patrón:

```python
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    inicializar_tabla_x(cursor)
    ...
    conn.commit()
except Exception:
    conn.rollback()
finally:
    conn.close()
```

## Refactorizaciones futuras

### Nivel 1 — Conexiones SQLite
Implementar cuando: existan al menos 3 módulos con la misma lógica de conexión.
Acción: crear utils/database.py con:

```python
abrir_conexion()

cerrar_conexion()
```

### Nivel 2 — Adaptadores de mercado
Implementar cuando: se soporte un segundo proveedor además de NewsAPI.
Acción: crear mercado/adapters/ con:

- newsapi_adapter.py
- polygon_adapter.py
- alphavantage_adapter.py

### Nivel 3 — Cliente HTTP
Implementar cuando: existan 2 APIs diferentes consumidas por el sistema.
Acción: crear utils/http_client.py encargado de:

- requests
- timeout
- reintentos
- headers
- user-agent
- logs

### Nivel 4 — Validadores
Implementar cuando: se validen datos en más de 3 módulos.
Acción: crear utils/validators.py con:

- validar_url()
- validar_fecha()
- validar_json()
- validar_respuesta_api()

### Nivel 5 — Context Manager para SQLite
Implementar cuando: la apertura/cierre de conexiones se repita en varios módulos.
Acción: introducir patrón:

```python
with abrir_conexion() as cursor:
    ...
```
#### Nivel 6 — Caché
Implementar cuando: varias APIs consulten la misma información.
Acción: crear utils/cache.py.

### Nivel 7 — Métricas
Implementar cuando: se requiera registrar automáticamente métricas de ejecución.
Acción: registrar:

- Tiempo de ejecución
- Noticias procesadas
- Noticias nuevas
- Noticias descartadas
- Errores
- Tiempo de respuesta API