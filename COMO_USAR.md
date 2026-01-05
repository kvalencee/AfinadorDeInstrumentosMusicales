# 🚀 GUÍA RÁPIDA DE USO - Afinador de Instrumentos

## ¿Qué hace este proyecto?

Analiza archivos de audio de instrumentos musicales (guitarra, piano, violín) y detecta:
- ✅ La nota musical que se está tocando
- ✅ La frecuencia fundamental
- ✅ Qué tan afinado está (en "cents")
- ✅ Los armónicos presentes

Todo usando **Procesamiento Digital de Señales (DSP)** con la **Transformada de Fourier (FFT)**.

---

## 📦 Instalación (SOLO UNA VEZ)

```bash
cd /Users/kvalencee/Documents/escom/instrumentos
pip install -r requirements.txt
```

Ya está instalado ✓

---

## 🎮 FORMAS DE USAR EL PROYECTO

### 1️⃣ INTERFAZ GRÁFICA (Más fácil)

```bash
python tuner_gui.py
```

**Pasos:**
1. Se abre una ventana con tema oscuro
2. Haz clic en "📁 Seleccionar Archivo de Audio"
3. Elige un archivo WAV (hay ejemplos en la carpeta `samples/`)
4. Haz clic en "🔍 Analizar"
5. ¡Listo! Verás la nota, frecuencia, desviación y la forma de onda

---

### 2️⃣ ANÁLISIS SIMPLE (Línea de comandos)

```bash
python audio_analyzer.py samples/A4_440Hz.wav
```

**Salida:**
```
Analyzing: samples/A4_440Hz.wav
------------------------------------------------------------
Detected Frequency: 440.00 Hz
Closest Note: A4
Exact Frequency: 440.00 Hz
Deviation: +0.0 cents
Status: En tono ✓
Duration: 2.00 seconds
```

---

### 3️⃣ ANÁLISIS AVANZADO CON DSP (Para tu materia)

```bash
python spectral_analysis.py samples/A4_440Hz.wav
```

**Esto muestra:**
- 📊 Parámetros de la señal (frecuencia de muestreo, número de muestras, resolución)
- 🎵 Frecuencia fundamental y nota detectada
- 🎼 Armónicos encontrados (múltiplos de la frecuencia fundamental)
- ✓ Conceptos de DSP aplicados

**Opcionalmente** puedes ver gráficos del espectro de frecuencias.

---

## 📁 Archivos de Prueba Incluidos

Ya se generaron 6 archivos de prueba en `samples/`:

| Archivo | Frecuencia | Descripción |
|---------|------------|-------------|
| `A4_440Hz.wav` | 440 Hz | La perfecta (referencia) |
| `E2_82Hz_guitar.wav` | 82.41 Hz | Cuerda grave de guitarra |
| `C4_262Hz_middle_c.wav` | 261.63 Hz | Do central del piano |
| `G3_196Hz_violin.wav` | 196 Hz | Sol de violín |
| `A4_445Hz_sharp.wav` | 445 Hz | La desafinada (aguda) |
| `A4_435Hz_flat.wav` | 435 Hz | La desafinada (grave) |

---

## 🎯 EJEMPLOS RÁPIDOS

### Probar todos los archivos de muestra:

```bash
# Análisis simple
python audio_analyzer.py samples/A4_440Hz.wav
python audio_analyzer.py samples/E2_82Hz_guitar.wav
python audio_analyzer.py samples/C4_262Hz_middle_c.wav

# Análisis avanzado con DSP
python spectral_analysis.py samples/A4_440Hz.wav
python spectral_analysis.py samples/A4_445Hz_sharp.wav
python spectral_analysis.py samples/A4_435Hz_flat.wav
```

### Usar tus propios archivos:

1. **Graba un audio** de tu instrumento en formato WAV
2. **Guárdalo** en la carpeta del proyecto
3. **Analízalo:**

```bash
python tuner_gui.py
# O
python spectral_analysis.py mi_audio.wav
```

---

## 📚 Archivos del Proyecto

```
instrumentos/
├── 🎨 tuner_gui.py              # Interfaz gráfica principal
├── 🔬 audio_analyzer.py         # Motor de análisis FFT
├── 📊 spectral_analysis.py      # Análisis avanzado con DSP
├── 🎵 note_frequencies.py       # Base de datos de notas musicales
├── 🧪 generate_samples.py       # Generador de archivos de prueba
├── 📖 README.md                 # Documentación completa
├── 📚 DSP_TEORIA.md            # Teoría de DSP y Fourier
├── 📋 requirements.txt          # Dependencias de Python
└── 📁 samples/                  # Archivos de audio de prueba
    ├── A4_440Hz.wav
    ├── E2_82Hz_guitar.wav
    ├── C4_262Hz_middle_c.wav
    ├── G3_196Hz_violin.wav
    ├── A4_445Hz_sharp.wav
    └── A4_435Hz_flat.wav
```

---

## 🧠 Conceptos de DSP Implementados

Lee el archivo **`DSP_TEORIA.md`** para entender:

- ✅ Serie de Fourier y Transformada de Fourier
- ✅ Transformada Discreta de Fourier (DFT)
- ✅ Fast Fourier Transform (FFT)
- ✅ Teorema de Nyquist-Shannon
- ✅ Ventanas (Hamming, Hanning, Blackman)
- ✅ Spectral Leakage y cómo evitarlo
- ✅ Análisis espectral
- ✅ Detección de frecuencia fundamental
- ✅ Armónicos y timbre
- ✅ Conversión frecuencia → nota musical
- ✅ Resolución frecuencial

---

## ❓ Preguntas Frecuentes

### ¿Qué formatos de audio acepta?
Solo **WAV** por ahora. Si tienes MP3, conviértelo con Audacity o ffmpeg.

### ¿Cómo grabo un audio WAV?
- **Mac**: QuickTime Player → Archivo → Nueva grabación de audio
- **Windows**: Grabadora de Voz
- **Multiplataforma**: Audacity (gratis)

### ¿Por qué usa FFT en vez de DFT?
FFT es mucho más rápida: O(N log N) vs O(N²). Para 88,200 muestras:
- DFT: ~7.8 mil millones de operaciones
- FFT: ~1.4 millones de operaciones

### ¿Qué es un "cent"?
1 cent = 1/100 de un semitono. El oído humano puede detectar ~5-10 cents de diferencia.

---

## 🎓 Para tu Materia de DSP

### Demuestra que entiendes:

1. **Serie de Fourier**: Cualquier señal periódica es suma de senos/cosenos
2. **DFT**: Versión discreta para señales digitales
3. **FFT**: Algoritmo eficiente para calcular DFT
4. **Ventanas**: Reducen spectral leakage (Hamming en este proyecto)
5. **Nyquist**: fs ≥ 2·fmax (44100 Hz permite hasta 22050 Hz)
6. **Armónicos**: Múltiplos de la frecuencia fundamental

### Comandos para demostrar:

```bash
# Muestra todos los conceptos de DSP
python spectral_analysis.py samples/A4_440Hz.wav

# Compara afinado vs desafinado
python spectral_analysis.py samples/A4_440Hz.wav
python spectral_analysis.py samples/A4_445Hz_sharp.wav
```

---

## 🏆 Resumen Ejecutivo

### Para correr el proyecto:

```bash
# Opción 1: GUI (recomendado)
python tuner_gui.py

# Opción 2: Análisis simple
python audio_analyzer.py samples/A4_440Hz.wav

# Opción 3: Análisis completo DSP
python spectral_analysis.py samples/A4_440Hz.wav
```

### Archivos importantes:
- **`DSP_TEORIA.md`** → Toda la teoría de Fourier y DSP
- **`README.md`** → Documentación completa del proyecto
- **`samples/`** → Archivos de prueba listos para usar

---

## 📞 Ayuda Rápida

Si algo no funciona:

```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt

# Regenerar archivos de prueba
python generate_samples.py

# Verificar que Python funciona
python --version  # Debe ser 3.7+
```

---

**¡Listo para usar! 🎉**

Fecha de entrega: **09 de enero 2026**
