# Instalación y Configuración

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.11 o superior
- Git (opcional)
- Ollama
- Conexión a Internet para descargar modelos y dependencias

# Clonar el Proyecto

git clone <https://github.com/Davleo89/trading_IA.git>
cd IA_Trading

O simplemente descarga el proyecto y descomprímelo en una carpeta local.

# Crear un Entorno Virtual

## Windows

Abrir PowerShell o CMD:

python -m venv venv

Activar el entorno:

venv\Scripts\activate

Si todo funciona correctamente verás:

(venv) C:\IA_Trading>

## Linux

Crear entorno virtual:

python3 -m venv venv

Activarlo:

source venv/bin/activate

Resultado esperado:

(venv) usuario@equipo:~/IA_Trading$

# Instalar Dependencias

## Actualizar pip:

python -m pip install --upgrade pip

## Instalar dependencias:

pip install pypdf
pip install sentence-transformers
pip install transformers
pip install torch
pip install numpy
pip install ollama

# Instalación de Ollama

## Windows

Descargar desde:

https://ollama.com

Instalar normalmente utilizando el asistente de instalación.

## Linux

Instalar mediante:

curl -fsSL https://ollama.com/install.sh | sh

Verificar instalación:

ollama --version

# Descargar Modelo LLM

Descargar Qwen:

ollama pull qwen2.5:3b

Verificar modelos instalados:

ollama list

# IA Trading Assistant

## Descripción

IA Trading Assistant es un proyecto personal desarrollado en Python cuyo objetivo es construir un asistente inteligente especializado en trading e inversiones.

La IA es capaz de leer libros en formato PDF, extraer conocimiento, almacenarlo en una base de datos, generar representaciones semánticas (embeddings) y responder preguntas utilizando modelos de lenguaje (LLM) ejecutados localmente.

El proyecto busca evolucionar desde una base de conocimiento teórica hasta una plataforma capaz de analizar mercados financieros, generar señales de trading y asistir en la toma de decisiones de inversión.

---

# Objetivos del Proyecto

## Objetivo Principal

Desarrollar una IA especializada en trading que pueda:

* Aprender conceptos a partir de libros y documentación.
* Responder preguntas sobre trading e inversiones.
* Analizar datos históricos y en tiempo real.
* Identificar patrones de mercado.
* Generar señales de compra, venta o espera.
* Explicar el razonamiento detrás de cada decisión.
* Funcionar localmente sin depender de servicios externos.

---

# Tecnologías Utilizadas

## Lenguaje

* Python

## Base de Datos

* SQLite

## Procesamiento de PDFs

* pypdf

## Embeddings

* sentence-transformers
* all-MiniLM-L6-v2

## Modelos de Lenguaje

* Ollama
* Qwen 2.5

## Procesamiento Numérico

* NumPy

## Machine Learning

* PyTorch (planificado)
* Scikit-Learn (planificado)

---

# Arquitectura Actual

PDFs
↓
Extracción de texto
↓
SQLite
↓
Chunks
↓
Embeddings
↓
Búsqueda semántica
↓
Qwen 2.5
↓
Respuesta al usuario

---

# Estado Actual del Proyecto

## Completado

* Lectura automática de PDFs.
* Clasificación por categorías.
* Almacenamiento del conocimiento en SQLite.
* División de documentos en chunks.
* Generación de embeddings.
* Búsqueda semántica.
* Integración con un modelo LLM local.
* Sistema RAG funcional.

## En Desarrollo

* Mejorar recuperación de contexto.
* Memoria conversacional.
* Optimización de búsquedas.

---

# Estructura del Proyecto

IA_Trading/

├── cargar_libros.py

├── chunks_embeddings.py

├── consultar_ia.py

├── libros_trading.db

└── pdf_books/

---

# Hoja de Ruta (Roadmap)

## Fase 1 - Base de Conocimiento ✅

* Leer PDFs.
* Almacenar conocimiento.
* Generar embeddings.
* Consultar información mediante IA.

## Fase 2 - Memoria Conversacional

* Recordar preguntas anteriores.
* Mantener contexto durante una conversación.
* Mejorar coherencia en respuestas extensas.

## Fase 3 - Motor de Análisis de Mercado

* Integrar datos históricos.
* Integrar datos de mercado en tiempo real.
* Analizar acciones e índices.
* Detectar tendencias.

## Fase 4 - Indicadores Técnicos

* RSI
* MACD
* SMA
* EMA
* Bandas de Bollinger
* Volumen
* Soportes y resistencias

## Fase 5 - Predicción de Señales

* Entrenamiento de modelos de Machine Learning.
* Generación de señales de compra.
* Generación de señales de venta.
* Evaluación de riesgo.

## Fase 6 - Agente Autónomo

* Monitoreo continuo del mercado.
* Alertas automáticas.
* Recomendaciones personalizadas.
* Explicación de decisiones.

## Fase 7 - Asistente Multiplataforma

* Aplicación de escritorio.
* Aplicación móvil.
* Comandos por voz.
* Integración con asistentes personales.

---

# Visión a Largo Plazo

El objetivo final es construir un asistente de trading inteligente inspirado en sistemas conversacionales avanzados, capaz de combinar:

* Conocimiento teórico.
* Análisis técnico.
* Gestión de riesgo.
* Psicología del trading.
* Datos de mercado en tiempo real.

La IA deberá actuar como un asistente de apoyo para el análisis financiero, proporcionando explicaciones transparentes y fundamentadas para cada recomendación generada.

---

# Autor

Proyecto desarrollado por Davleo como iniciativa de aprendizaje en Inteligencia Artificial, Procesamiento de Lenguaje Natural (NLP), Machine Learning y Trading Algorítmico.

