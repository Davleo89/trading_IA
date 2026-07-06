import time
import argparse

# ==========================================
# IMPORTS DE MODULOS DEL PIPELINE
# ==========================================

import leer_pdf
import crear_chunks
import crear_embeddings
import generar_resumenes
import clasificador_libros

#===========================================
# FUNCIONES AUXILIARES
#===========================================

def ejecutar_paso(nombre, funcion):
    print("\n" + "=" * 60)
    print(f"📌 Ejecutando paso: {nombre}")
    
    try:
        if funcion:            
            funcion()
        else:
            print("⚠️ No se proporcionó ninguna función para ejecutar.")
            time.sleep(1)
            
        print(f"✅ Paso '{nombre}' ejecutado correctamente.")
        return True
        
    except Exception as e:
        print(f"✗ ERROR en el paso: {nombre}")
        print(f"  Tipo de error: {type(e).__name__}")
        print(f"  Descripción:   {e}")
        
        return False
    
#===========================================
# FLUJO PRINCIPAL (PIPELINE)
#===========================================

def main():
    print("\n" + "=" * 60)
    print("🚀 PIPELINE - BIBLIOTECA IA TRADING")
    
    # La lista de diccionarios (Configuración limpia)
    pasos = [
        {    
            "id_code": "leer_pdf",
            "nombre": "Leer PDFs",
            "funcion": leer_pdf.main,
        },
        {
            "id_code": "crear_chunks",
            "nombre": "Crear Chunks",
            "funcion": crear_chunks.main
        },
        {
            "id_code": "crear_embeddings",
            "nombre": "Crear Embeddings",
            "funcion": crear_embeddings.main
        },
        {
            "id_code": "resumenes",
            "nombre": "Generar Resúmenes",
            "funcion": generar_resumenes.main
        },
        {
            "id_code": "clasificador",
            "nombre": "Clasificar Libros",
            "funcion": clasificador_libros.main
        }
    ]
    
    parser = argparse.ArgumentParser(
        description = "🚀 Motor del Pipeline - Biblioteca IA Trading"
    )
    parser.add_argument(
        "--listar", 
        action = "store_true", 
        help = "Muestra los identificadores de los pasos disponibles."
    )
    parser.add_argument(
        "--paso", 
        type = str, 
        help = "Ejecuta un único paso específico usando su id."
    )
    
    args = parser.parse_args()

    # CORRECCIÓN DETALLE 1: El bucle ahora itera sobre el objeto 'paso'
    if args.listar:
        print("\n" + "=" * 50)
        print("📋 PASOS DISPONIBLES EN EL PIPELINE:")
        print("=" * 50)
        for paso in pasos:
            print(f"  • {paso['id_code']:<12} -> {paso['nombre']}")
        print("=" * 50 + "\n")
        return

    if args.paso:
        paso_filtrado = [p for p in pasos if p["id_code"] == args.paso]
        
        if not paso_filtrado:
            print(f"❌ Error: El paso '{args.paso}' no existe.")
            print("Usa 'python src\\pipeline.py --listar' para ver las opciones válidas.")
            return
        
        pasos = paso_filtrado
    
    inicio = time.time()
    
    # CORRECCIÓN DETALLE 2: Eliminado el desempaquetado posicional antiguo
    for paso in pasos:
        exito = ejecutar_paso(paso["nombre"], paso["funcion"])
        
        if not exito:
            print("=" * 60)
            print(f"🛑 PIPELINE ABORTADO: Fallo crítico en el paso '{paso['nombre']}'.")
            print("Se detuvo la ejecución para proteger la integridad del sistema.")
            print("=" * 60)
            return
        
    fin = time.time()
    tiempo_total = fin - inicio
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print(f"⏱️ Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    print("\n" + "=" * 60)
    
if __name__ == "__main__":
    main()