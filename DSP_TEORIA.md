# 📚 Fundamentos Teóricos - Procesamiento Digital de Señales

## Conceptos de DSP Implementados

Este proyecto implementa varios conceptos fundamentales de **Procesamiento Digital de Señales (DSP)**:

---

## 1. Serie de Fourier y Transformada de Fourier

### Serie de Fourier

Cualquier señal periódica puede descomponerse en una suma de senos y cosenos:

```
x(t) = a₀ + Σ(n=1 to ∞) [aₙ·cos(nω₀t) + bₙ·sin(nω₀t)]
```

Donde:
- `a₀` = componente DC (valor promedio)
- `aₙ, bₙ` = coeficientes de Fourier
- `ω₀ = 2πf₀` = frecuencia angular fundamental
- `n` = número del armónico

### Transformada Discreta de Fourier (DFT)

Para señales digitales (muestreadas), usamos la DFT:

```
X[k] = Σ(n=0 to N-1) x[n] · e^(-j·2π·k·n/N)
```

Donde:
- `x[n]` = señal en el dominio del tiempo
- `X[k]` = señal en el dominio de la frecuencia
- `N` = número de muestras
- `k` = índice de frecuencia
- `j` = unidad imaginaria (√-1)

### Fast Fourier Transform (FFT)

La FFT es un algoritmo eficiente para calcular la DFT:
- **Complejidad DFT**: O(N²)
- **Complejidad FFT**: O(N log N)

En Python usamos `scipy.fft.rfft()` que calcula solo las frecuencias positivas (señales reales).

---

## 2. Teorema de Muestreo de Nyquist-Shannon

Para reconstruir perfectamente una señal, la frecuencia de muestreo debe ser:

```
fs ≥ 2 · fmax
```

Donde:
- `fs` = frecuencia de muestreo
- `fmax` = frecuencia máxima en la señal

**En este proyecto:**
- Usamos `fs = 44100 Hz` (estándar de audio CD)
- Podemos detectar frecuencias hasta `fmax = 22050 Hz`
- Las notas musicales van de ~16 Hz a ~4200 Hz ✓

---

## 3. Ventanas (Windowing)

### Problema: Spectral Leakage

Cuando analizamos una señal de duración finita, aparece "fuga espectral" que distorsiona el espectro.

### Solución: Funciones de Ventana

Aplicamos una ventana que suaviza los bordes de la señal:

#### Ventana de Hamming (usada en este proyecto)

```
w[n] = 0.54 - 0.46·cos(2πn/(N-1))
```

**Características:**
- Reduce el lóbulo lateral en -43 dB
- Buen balance entre resolución y fuga espectral
- Ideal para análisis de audio musical

#### Otras ventanas disponibles:

- **Hanning**: `w[n] = 0.5 - 0.5·cos(2πn/(N-1))`
- **Blackman**: Mayor atenuación pero menor resolución

---

## 4. Análisis Espectral

### Magnitud del Espectro

```
|X[k]| = √(Re(X[k])² + Im(X[k])²)
```

La magnitud nos dice la "intensidad" de cada componente de frecuencia.

### Fase del Espectro

```
φ[k] = arctan(Im(X[k]) / Re(X[k]))
```

La fase indica el desplazamiento temporal de cada componente.

### Frecuencias Correspondientes

```
f[k] = k · fs / N
```

Donde:
- `k` = índice (0, 1, 2, ..., N/2)
- `fs` = frecuencia de muestreo
- `N` = número de muestras

---

## 5. Detección de Frecuencia Fundamental

### Método: Peak Picking

1. **Calcular FFT** de la señal
2. **Encontrar el pico** de mayor magnitud en el rango musical (20-5000 Hz)
3. **Ese pico corresponde** a la frecuencia fundamental (f₀)

### Código implementado:

```python
# Calcular FFT
fft_values = rfft(windowed_signal)
frequencies = rfftfreq(N, 1/sample_rate)
magnitude = np.abs(fft_values)

# Encontrar pico máximo
peak_idx = np.argmax(magnitude[min_idx:max_idx])
fundamental_freq = frequencies[peak_idx]
```

---

## 6. Armónicos

### Teoría

Los instrumentos musicales producen no solo la frecuencia fundamental, sino también **armónicos**:

```
f₁ = f₀           (fundamental)
f₂ = 2·f₀         (segunda armónica)
f₃ = 3·f₀         (tercera armónica)
...
fₙ = n·f₀         (n-ésima armónica)
```

**El timbre** de un instrumento depende de la intensidad relativa de estos armónicos.

### Ejemplo: Nota A4 (440 Hz)

- f₀ = 440 Hz (fundamental)
- f₂ = 880 Hz (octava)
- f₃ = 1320 Hz (quinta + octava)
- f₄ = 1760 Hz (dos octavas)

---

## 7. Conversión Frecuencia → Nota Musical

### Escala Temperada

La escala musical occidental usa **temperamento igual** con 12 semitonos por octava:

```
f(n) = f₀ · 2^(n/12)
```

Donde:
- `f₀ = 440 Hz` (A4, referencia estándar)
- `n` = número de semitonos desde A4

### Cents (Desviación de Afinación)

Un **cent** es 1/100 de un semitono:

```
cents = 1200 · log₂(f_detectada / f_nota_exacta)
```

**Interpretación:**
- `0 cents` = perfectamente afinado
- `+50 cents` = medio semitono agudo
- `-50 cents` = medio semitono grave
- `±10 cents` = generalmente aceptable

---

## 8. Resolución Frecuencial

La resolución en frecuencia depende de la duración de la señal:

```
Δf = fs / N = 1 / T
```

Donde:
- `T` = duración de la señal en segundos
- `N` = número de muestras
- `fs` = frecuencia de muestreo

**Ejemplo:**
- Si `T = 2 segundos` y `fs = 44100 Hz`
- Entonces `N = 88200 muestras`
- Resolución: `Δf = 44100/88200 = 0.5 Hz` ✓

**Implicación:** Señales más largas → mejor resolución frecuencial

---

## 9. Implementación en el Proyecto

### Archivo: `audio_analyzer.py`

```python
def get_fundamental_frequency(audio_data, sample_rate):
    # 1. Aplicar ventana de Hamming
    window = np.hamming(len(audio_data))
    windowed_data = audio_data * window
    
    # 2. Calcular FFT
    fft_data = fft(windowed_data)
    fft_freqs = fftfreq(len(windowed_data), 1/sample_rate)
    
    # 3. Obtener magnitud
    magnitude = np.abs(fft_data)
    
    # 4. Encontrar pico (frecuencia fundamental)
    peak_idx = np.argmax(magnitude[range_musical])
    fundamental_freq = fft_freqs[peak_idx]
    
    return fundamental_freq
```

### Archivo: `spectral_analysis.py`

Análisis avanzado que muestra:
- ✅ Frecuencia fundamental
- ✅ Armónicos detectados
- ✅ Espectro completo de frecuencias
- ✅ Parámetros de la señal (fs, N, resolución)

---

## 10. Diagrama del Proceso

```
Audio WAV (señal analógica digitalizada)
         ↓
    [Muestreo a fs = 44100 Hz]
         ↓
    Señal Digital x[n]
         ↓
    [Aplicar Ventana de Hamming]
         ↓
    Señal Ventaneada
         ↓
    [FFT - Transformada Rápida de Fourier]
         ↓
    Espectro X[k] (dominio de frecuencia)
         ↓
    [Calcular Magnitud |X[k]|]
         ↓
    [Detectar Pico Máximo]
         ↓
    Frecuencia Fundamental f₀
         ↓
    [Comparar con Tabla de Notas]
         ↓
    Nota Musical + Desviación (cents)
```

---

## Referencias Teóricas

### Libros Recomendados:
1. **Oppenheim & Schafer** - "Discrete-Time Signal Processing"
2. **Proakis & Manolakis** - "Digital Signal Processing: Principles, Algorithms, and Applications"
3. **Smith** - "The Scientist and Engineer's Guide to Digital Signal Processing"

### Fórmulas Clave:

| Concepto | Fórmula |
|----------|---------|
| DFT | `X[k] = Σ x[n]·e^(-j2πkn/N)` |
| FFT Inversa | `x[n] = (1/N)·Σ X[k]·e^(j2πkn/N)` |
| Frecuencia | `f[k] = k·fs/N` |
| Nyquist | `fs ≥ 2·fmax` |
| Resolución | `Δf = fs/N = 1/T` |
| Cents | `cents = 1200·log₂(f/f₀)` |

---

## Conclusión

Este proyecto implementa un **sistema completo de análisis espectral** usando:

✅ **Transformada de Fourier** (vía FFT)  
✅ **Ventanas de Hamming** (reducción de spectral leakage)  
✅ **Detección de frecuencia fundamental**  
✅ **Análisis de armónicos**  
✅ **Conversión frecuencia-nota musical**  
✅ **Cálculo de desviación en cents**  

Todos estos son conceptos fundamentales en **Procesamiento Digital de Señales** aplicados a un problema real de análisis de audio musical.
