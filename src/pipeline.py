import time
import argparse

# ==========================================
# IMPORTS DE MÓDULOS DEL PIPELINE
# ==========================================
from utils import logger

import biblioteca.leer_pdf as leer_pdf
import biblioteca.crear_chunks as crear_chunks
import biblioteca.crear_embeddings as crear_embeddings
import biblioteca.generar_resumenes as generar_resumenes
import biblioteca.clasificador_libros as clasificador_libros

#===========================================
# FUNCIONES AUXILIARES
#===========================================

def ejecutar_paso(nombre, funcion):
    logger.escribir_log(f"Ejecutando paso: {nombre}", nivel="info")
    
    try:
        if funcion:            
            funcion()
        else:
            logger.escribir_log(nivel="info")
            time.sleep(1)
            
        logger.escribir_log(f"Paso '{nombre}' ejecutado correctamente.", nivel="success")
        return True
        
    except Exception as e:
        mensaje_error = (
            f"ERROR CRÍTICO en el paso '{nombre}'\n"
            f"  -> Tipo de error: {type(e).__name__}\n"
            f"  -> Descripción:   {e}"
        )
        logger.escribir_log(mensaje_error, nivel="error")
        return False
    
#===========================================
# FLUJO PRINCIPAL (PIPELINE)
#===========================================

def main():

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
            print("Usa 'python src/pipeline.py --listar' para ver las opciones válidas.")
            return
        
        pasos = paso_filtrado

    # ==================================================
    # ADQUISICIÓN DE RECURSOS Y OPERACIÓN SEGURA
    # ==================================================
    
    logger.crear_archivo_log()
    inicio = time.time()
    
    try:
        logger.escribir_log("🚀 PIPELINE - BIBLIOTECA IA TRADING INICIADO", nivel="info")
        
        for paso in pasos:
            exito = ejecutar_paso(paso["nombre"], paso["funcion"])
            
            if not exito:
                logger.escribir_log(f"🛑 PIPELINE ABORTADO: Fallo crítico en el paso '{paso['nombre']}'.", nivel="error")
                logger.escribir_log("Se detuvo la ejecución para proteger la integridad del sistema.", nivel="error")
                return
            
        fin = time.time()
        tiempo_total = fin - inicio
        
        logger.escribir_log("📊 RESUMEN FINAL", nivel="info")
        logger.escribir_log(f"⏱️ Tiempo total de ejecución: {tiempo_total:.2f} segundos", nivel="success")
        
    except Exception as e_inesperado:
        
        logger.escribir_log(f"💥 EXCEPCIÓN INESPERADA EN EL NÚCLEO DEL PIPELINE: {e_inesperado}", nivel="error")
        
    finally:
        
        logger.cerrar_log()

if __name__ == "__main__":
    main()