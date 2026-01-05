# 🎵 Afinador de Instrumentos Musicales

**Proyecto 1 - ESCOM**  
Fecha de entrega: 09 de enero 2026

## Descripción

Aplicación en Python con interfaz gráfica que permite subir archivos de audio de instrumentos musicales (guitarra, piano o violín) y detecta las notas musicales tocadas mediante análisis FFT (Fast Fourier Transform).

### Características

- ✅ Detección de notas musicales usando análisis FFT
- ✅ Identificación de frecuencia fundamental
- ✅ Comparación con frecuencias estándar de notas musicales
- ✅ Cálculo de desviación en cents
- ✅ Visualización de forma de onda
- ✅ Interfaz gráfica moderna y fácil de usar
- ✅ Indicador visual de afinación (en tono, agudo, grave)

## Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `numpy`: Operaciones numéricas y FFT
- `scipy`: Procesamiento de señales y lectura de archivos WAV
- `matplotlib`: Visualización de forma de onda
- `tkinter`: Interfaz gráfica (incluido con Python)

## Uso

### Ejecutar la Aplicación

```bash
python tuner_gui.py
```

### Pasos para Analizar Audio

1. **Seleccionar archivo**: Haz clic en "📁 Seleccionar Archivo de Audio"
2. **Elegir archivo WAV**: Selecciona un archivo de audio en formato WAV
3. **Analizar**: Haz clic en "🔍 Analizar"
4. **Ver resultados**: La aplicación mostrará:
   - Nota musical detectada (grande y centrada)
   - Frecuencia fundamental detectada
   - Frecuencia exacta de la nota estándar
   - Desviación en cents
   - Estado de afinación (en tono, agudo, grave)
   - Visualización de la forma de onda

### Análisis desde Línea de Comandos

También puedes analizar archivos directamente desde la terminal:

```bash
python audio_analyzer.py archivo.wav
```

## Cómo Funciona

### Análisis FFT

1. **Carga del audio**: El archivo WAV se carga y convierte a mono si es estéreo
2. **Ventana de análisis**: Se aplica una ventana Hamming para reducir el "spectral leakage"
3. **Transformada de Fourier**: Se calcula la FFT para obtener el espectro de frecuencias
4. **Detección de pico**: Se identifica la frecuencia con mayor magnitud (frecuencia fundamental)
5. **Identificación de nota**: Se compara con las frecuencias estándar de notas musicales
6. **Cálculo de desviación**: Se calcula cuántos cents se desvía de la afinación perfecta

### Fórmula de Cents

La desviación en cents se calcula usando:

```
cents = 1200 × log₂(f_detectada / f_nota_exacta)
```

Donde:
- 100 cents = 1 semitono
- ±10 cents = generalmente considerado "en tono"

## Estructura del Proyecto

```
instrumentos/
├── tuner_gui.py           # Aplicación principal con interfaz gráfica
├── audio_analyzer.py      # Módulo de análisis de audio y FFT
├── note_frequencies.py    # Referencia de frecuencias de notas musicales
├── requirements.txt       # Dependencias de Python
└── README.md             # Este archivo
```

## Formatos de Audio Soportados

- **WAV** (recomendado): Formato sin compresión, mejor calidad para análisis

> **Nota**: Para otros formatos (MP3, FLAC, etc.), primero conviértelos a WAV usando herramientas como Audacity o ffmpeg.

## Rangos de Instrumentos

- **Guitarra**: E2 (82.41 Hz) a D6 (1174.66 Hz)
- **Piano**: A0 (27.50 Hz) a C8 (4186.01 Hz)
- **Violín**: G3 (196.00 Hz) a G7 (3135.96 Hz)

## Interpretación de Resultados

### Estado de Afinación

- **En tono ✓** (verde): Desviación < ±10 cents
- **Agudo (sostenido)** (naranja/amarillo): Frecuencia más alta que la nota
- **Grave (bemol)** (rojo): Frecuencia más baja que la nota

### Colores de Desviación

- 🟢 Verde: < ±10 cents (bien afinado)
- 🟡 Naranja: ±10 a ±30 cents (ligeramente desafinado)
- 🔴 Rojo: > ±30 cents (muy desafinado)

## Ejemplos de Uso

### Crear un Archivo de Prueba

Puedes grabar notas de tu instrumento usando cualquier software de grabación (Audacity, GarageBand, etc.) y guardarlas como WAV.

### Probar el Analizador

```bash
# Probar con un archivo específico
python audio_analyzer.py mi_guitarra.wav
```

Salida esperada:
```
Analyzing: mi_guitarra.wav
------------------------------------------------------------
Detected Frequency: 329.63 Hz
Closest Note: E4
Exact Frequency: 329.63 Hz
Deviation: +0.0 cents
Status: En tono ✓
Duration: 2.50 seconds
```

## Solución de Problemas

### Error al cargar archivo

- Verifica que el archivo sea formato WAV
- Asegúrate de que el archivo no esté corrupto
- Intenta convertir el archivo a WAV con otra herramienta

### Frecuencia detectada incorrecta

- Asegúrate de que el audio tenga buena calidad
- Evita ruido de fondo
- Graba notas sostenidas (al menos 1-2 segundos)
- Verifica que el volumen sea adecuado (ni muy bajo ni saturado)

### La interfaz no se muestra

- Verifica que tkinter esté instalado (viene con Python en la mayoría de los casos)
- En Linux, puede que necesites: `sudo apt-get install python3-tk`

## Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación
- **NumPy**: Cálculos numéricos y FFT
- **SciPy**: Procesamiento de señales
- **Matplotlib**: Visualización de datos
- **Tkinter**: Interfaz gráfica de usuario

## Autor

Proyecto desarrollado para ESCOM - Escuela Superior de Cómputo

## Licencia

Este proyecto es para fines educativos.
