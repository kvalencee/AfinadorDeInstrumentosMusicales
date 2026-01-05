"""
Análisis Espectral Avanzado - Procesamiento Digital de Señales
Demuestra conceptos de DSP: Serie de Fourier, FFT, Espectro de Frecuencias
"""

import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import matplotlib.pyplot as plt
from note_frequencies import get_note_from_frequency, format_note_name


class SpectralAnalyzer:
    """
    Analizador espectral que implementa conceptos de DSP:
    - Transformada Discreta de Fourier (DFT) vía FFT
    - Análisis de espectro de frecuencias
    - Detección de armónicos
    """
    
    def __init__(self, audio_file):
        """
        Inicializa el analizador con un archivo de audio
        
        Args:
            audio_file (str): Ruta al archivo WAV
        """
        self.sample_rate, audio_data = wavfile.read(audio_file)
        
        # Convertir a mono si es estéreo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalizar
        if audio_data.dtype == np.int16:
            audio_data = audio_data.astype(np.float32) / 32768.0
        elif audio_data.dtype == np.int32:
            audio_data = audio_data.astype(np.float32) / 2147483648.0
        
        self.audio_data = audio_data
        self.duration = len(audio_data) / self.sample_rate
        self.N = len(audio_data)  # Número de muestras
        
    def compute_fft(self, window='hamming'):
        """
        Calcula la FFT (Fast Fourier Transform) de la señal
        
        La FFT es una implementación eficiente de la DFT (Discrete Fourier Transform)
        que descompone la señal en sus componentes de frecuencia.
        
        Fórmula DFT: X[k] = Σ(n=0 to N-1) x[n] * e^(-j*2π*k*n/N)
        
        Args:
            window (str): Tipo de ventana ('hamming', 'hanning', 'blackman', 'none')
            
        Returns:
            tuple: (frequencies, magnitude, phase)
        """
        # Aplicar ventana para reducir "spectral leakage"
        if window == 'hamming':
            w = np.hamming(self.N)
        elif window == 'hanning':
            w = np.hanning(self.N)
        elif window == 'blackman':
            w = np.blackman(self.N)
        else:
            w = np.ones(self.N)
        
        windowed_signal = self.audio_data * w
        
        # Calcular FFT (solo frecuencias positivas con rfft)
        fft_values = rfft(windowed_signal)
        frequencies = rfftfreq(self.N, 1/self.sample_rate)
        
        # Magnitud y fase
        magnitude = np.abs(fft_values)
        phase = np.angle(fft_values)
        
        return frequencies, magnitude, phase
    
    def find_fundamental_and_harmonics(self, num_harmonics=5):
        """
        Encuentra la frecuencia fundamental y sus armónicos
        
        En teoría musical, los armónicos son múltiplos enteros de la frecuencia fundamental:
        f_n = n * f_0, donde n = 1, 2, 3, ...
        
        Args:
            num_harmonics (int): Número de armónicos a detectar
            
        Returns:
            dict: Información sobre fundamental y armónicos
        """
        freqs, magnitude, _ = self.compute_fft()
        
        # Buscar picos en el rango de frecuencias musicales (20 Hz - 5000 Hz)
        min_idx = np.argmax(freqs > 20)
        max_idx = np.argmax(freqs > 5000)
        if max_idx == 0:
            max_idx = len(freqs)
        
        # Encontrar la frecuencia fundamental (pico más alto)
        search_magnitude = magnitude[min_idx:max_idx]
        search_freqs = freqs[min_idx:max_idx]
        
        fundamental_idx = np.argmax(search_magnitude)
        fundamental_freq = search_freqs[fundamental_idx]
        
        # Buscar armónicos (múltiplos de la fundamental)
        harmonics = []
        for n in range(2, num_harmonics + 1):
            harmonic_freq = n * fundamental_freq
            
            # Buscar el pico más cercano a la frecuencia armónica esperada
            tolerance = 50  # Hz
            harmonic_range = np.where(
                (freqs >= harmonic_freq - tolerance) & 
                (freqs <= harmonic_freq + tolerance)
            )[0]
            
            if len(harmonic_range) > 0:
                harmonic_idx = harmonic_range[np.argmax(magnitude[harmonic_range])]
                harmonics.append({
                    'order': n,
                    'frequency': freqs[harmonic_idx],
                    'magnitude': magnitude[harmonic_idx],
                    'expected': harmonic_freq
                })
        
        # Identificar nota musical
        note, exact_freq, cents = get_note_from_frequency(fundamental_freq)
        
        return {
            'fundamental': {
                'frequency': fundamental_freq,
                'magnitude': magnitude[min_idx + fundamental_idx],
                'note': note,
                'note_formatted': format_note_name(note),
                'exact_frequency': exact_freq,
                'cents': cents
            },
            'harmonics': harmonics,
            'sample_rate': self.sample_rate,
            'num_samples': self.N
        }
    
    def plot_spectrum(self, max_freq=2000, save_path=None):
        """
        Grafica el espectro de frecuencias
        
        Args:
            max_freq (float): Frecuencia máxima a mostrar
            save_path (str): Ruta para guardar la imagen (opcional)
        """
        freqs, magnitude, _ = self.compute_fft()
        
        # Limitar a frecuencias de interés
        idx_max = np.argmax(freqs > max_freq)
        if idx_max == 0:
            idx_max = len(freqs)
        
        plt.figure(figsize=(12, 6))
        
        # Subplot 1: Espectro completo
        plt.subplot(2, 1, 1)
        plt.plot(freqs[:idx_max], magnitude[:idx_max], color='#00d4ff', linewidth=1)
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud')
        plt.title('Espectro de Frecuencias (FFT)')
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Señal en el tiempo
        plt.subplot(2, 1, 2)
        time = np.linspace(0, self.duration, self.N)
        # Mostrar solo una porción si es muy largo
        max_samples = 10000
        if self.N > max_samples:
            step = self.N // max_samples
            time = time[::step]
            audio_plot = self.audio_data[::step]
        else:
            audio_plot = self.audio_data
        
        plt.plot(time, audio_plot, color='#16c79a', linewidth=0.5)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.title('Señal en el Dominio del Tiempo')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Espectro guardado en: {save_path}")
        else:
            plt.show()
    
    def print_analysis(self):
        """Imprime un análisis completo de la señal"""
        result = self.find_fundamental_and_harmonics()
        
        print("=" * 70)
        print("ANÁLISIS ESPECTRAL - PROCESAMIENTO DIGITAL DE SEÑALES")
        print("=" * 70)
        print(f"\n📊 Parámetros de la señal:")
        print(f"   • Frecuencia de muestreo (fs): {self.sample_rate} Hz")
        print(f"   • Número de muestras (N): {self.N}")
        print(f"   • Duración: {self.duration:.3f} segundos")
        print(f"   • Resolución frecuencial: {self.sample_rate/self.N:.2f} Hz")
        
        fund = result['fundamental']
        print(f"\n🎵 Frecuencia Fundamental (f₀):")
        print(f"   • Frecuencia detectada: {fund['frequency']:.2f} Hz")
        print(f"   • Nota musical: {fund['note_formatted']}")
        print(f"   • Frecuencia exacta de la nota: {fund['exact_frequency']:.2f} Hz")
        print(f"   • Desviación: {fund['cents']:+.1f} cents")
        print(f"   • Magnitud: {fund['magnitude']:.2f}")
        
        if result['harmonics']:
            print(f"\n🎼 Armónicos detectados:")
            print(f"   {'Orden':<8} {'Frecuencia':<15} {'Esperada':<15} {'Magnitud':<12}")
            print(f"   {'-'*8} {'-'*15} {'-'*15} {'-'*12}")
            for h in result['harmonics']:
                print(f"   {h['order']:<8} {h['frequency']:<15.2f} "
                      f"{h['expected']:<15.2f} {h['magnitude']:<12.2f}")
        
        print("\n" + "=" * 70)
        print("CONCEPTOS DE DSP APLICADOS:")
        print("=" * 70)
        print("✓ Transformada Rápida de Fourier (FFT)")
        print("✓ Ventana de Hamming (reducción de spectral leakage)")
        print("✓ Análisis espectral en frecuencia")
        print("✓ Detección de frecuencia fundamental")
        print("✓ Identificación de armónicos")
        print("✓ Teorema de Nyquist (fs > 2*f_max)")
        print("=" * 70 + "\n")


def main():
    """Función principal para demostración"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python spectral_analysis.py <archivo.wav>")
        print("\nEjemplo:")
        print("  python spectral_analysis.py samples/A4_440Hz.wav")
        return
    
    audio_file = sys.argv[1]
    
    print(f"\n🎵 Analizando: {audio_file}\n")
    
    # Crear analizador
    analyzer = SpectralAnalyzer(audio_file)
    
    # Imprimir análisis completo
    analyzer.print_analysis()
    
    # Preguntar si quiere ver el gráfico
    response = input("¿Deseas ver el gráfico del espectro? (s/n): ")
    if response.lower() == 's':
        analyzer.plot_spectrum(max_freq=2000)


if __name__ == "__main__":
    main()
