# 📦 Cómo Crear Ejecutables

## ✅ Ejecutable para macOS (Ya Creado)

El ejecutable para macOS ya está listo en: `dist/AfinadorMusical.app`

### Cómo usar:
1. Navega a la carpeta `dist/`
2. Haz doble clic en `AfinadorMusical.app`
3. Si macOS bloquea la app por seguridad:
   - Ve a **Preferencias del Sistema → Seguridad y Privacidad**
   - Haz clic en "Abrir de todos modos"
   - O ejecuta: `xattr -cr dist/AfinadorMusical.app`

---

## 🪟 Ejecutable para Windows

Para crear el ejecutable de Windows, necesitas ejecutar esto **en una máquina Windows**:

### Paso 1: Instalar dependencias en Windows
```bash
pip install pyinstaller numpy scipy matplotlib pyaudio
```

### Paso 2: Instalar PortAudio (para PyAudio)
Descarga e instala PortAudio desde: http://www.portaudio.com/

O usa el instalador pre-compilado:
```bash
pip install pipwin
pipwin install pyaudio
```

### Paso 3: Crear el ejecutable
```bash
pyinstaller --name="AfinadorMusical" --windowed --add-data="samples;samples" tuner_gui.py
```

**Nota**: En Windows usa `;` en vez de `:` para `--add-data`

### Paso 4: Resultado
El ejecutable estará en: `dist/AfinadorMusical/AfinadorMusical.exe`

---

## 📋 Archivos Incluidos

Ambos ejecutables incluyen:
- ✅ Todas las librerías de Python necesarias
- ✅ NumPy, SciPy, Matplotlib
- ✅ PyAudio para grabación en vivo
- ✅ Archivos de muestra en la carpeta `samples/`
- ✅ Interfaz gráfica completa

---

## 🚀 Distribución

### macOS
- Comprime `AfinadorMusical.app` en un ZIP
- Comparte el ZIP con otros usuarios de Mac
- Tamaño aproximado: ~80-100 MB

### Windows  
- Comprime la carpeta `dist/AfinadorMusical/` completa
- Comparte el ZIP con usuarios de Windows
- Tamaño aproximado: ~100-120 MB

---

## ⚠️ Notas Importantes

1. **macOS**: El ejecutable puede requerir permisos de micrófono la primera vez
2. **Windows**: Windows Defender puede marcar el ejecutable como desconocido (es normal)
3. **Ambos**: Los archivos de muestra están incluidos en la carpeta `samples/` dentro del ejecutable

---

## 🔧 Solución de Problemas

### macOS: "La aplicación está dañada"
```bash
xattr -cr dist/AfinadorMusical.app
```

### Windows: "Windows protegió tu PC"
- Haz clic en "Más información"
- Luego en "Ejecutar de todos modos"

### Ambos: No se puede acceder al micrófono
- Verifica los permisos del sistema
- En macOS: Preferencias → Seguridad → Micrófono
- En Windows: Configuración → Privacidad → Micrófono
