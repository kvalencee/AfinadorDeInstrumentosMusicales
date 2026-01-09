"""
Módulo de grabación de audio en vivo
Graba audio desde el micrófono para análisis en tiempo real
"""

import pyaudio
import wave
import numpy as np
import os
import tempfile
from datetime import datetime


class LiveRecorder:
    """Clase para grabar audio en vivo desde el micrófono"""
    
    def __init__(self, sample_rate=44100, channels=1, chunk_size=1024):
        """
        Inicializa el grabador de audio
        
        Args:
            sample_rate: Frecuencia de muestreo (Hz)
            channels: Número de canales (1=mono, 2=estéreo)
            chunk_size: Tamaño del buffer de audio
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16  # 16-bit audio
        self.audio = None
        self.stream = None
        
    def record(self, duration=3.0, output_file=None):
        """
        Graba audio desde el micrófono
        
        Args:
            duration: Duración de la grabación en segundos
            output_file: Ruta del archivo de salida (opcional)
            
        Returns:
            str: Ruta del archivo WAV generado
            
        Raises:
            Exception: Si hay problemas con el micrófono
        """
        try:
            # Inicializar PyAudio
            self.audio = pyaudio.PyAudio()
            
            # Abrir stream de audio
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            print(f"🎤 Grabando durante {duration} segundos...")
            
            # Calcular número de frames a grabar
            frames_to_record = int(self.sample_rate / self.chunk_size * duration)
            frames = []
            
            # Grabar audio
            for i in range(frames_to_record):
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
            
            print("✅ Grabación completada")
            
            # Detener y cerrar stream
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            
            # Generar nombre de archivo si no se proporcionó
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(tempfile.gettempdir(), f"live_recording_{timestamp}.wav")
            
            # Guardar como archivo WAV
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
            
            print(f"💾 Audio guardado en: {output_file}")
            return output_file
            
        except Exception as e:
            # Limpiar recursos en caso de error
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()
            raise Exception(f"Error al grabar audio: {str(e)}")
    
    def get_available_devices(self):
        """
        Obtiene la lista de dispositivos de audio disponibles
        
        Returns:
            list: Lista de dispositivos de entrada disponibles
        """
        try:
            audio = pyaudio.PyAudio()
            devices = []
            
            for i in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels']
                    })
            
            audio.terminate()
            return devices
            
        except Exception as e:
            print(f"Error al obtener dispositivos: {str(e)}")
            return []
    
    def test_microphone(self):
        """
        Prueba si el micrófono está disponible
        
        Returns:
            bool: True si el micrófono funciona, False en caso contrario
        """
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            # Leer un pequeño fragmento de audio
            stream.read(self.chunk_size, exception_on_overflow=False)
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            return True
            
        except Exception as e:
            print(f"❌ Micrófono no disponible: {str(e)}")
            return False


# Función de utilidad para grabación rápida
def quick_record(duration=3.0, output_file=None):
    """
    Función de utilidad para grabar audio rápidamente
    
    Args:
        duration: Duración en segundos
        output_file: Archivo de salida (opcional)
        
    Returns:
        str: Ruta del archivo WAV generado
    """
    recorder = LiveRecorder()
    return recorder.record(duration, output_file)


if __name__ == "__main__":
    # Prueba del módulo
    print("=== Prueba de Grabación en Vivo ===\n")
    
    recorder = LiveRecorder()
    
    # Verificar micrófono
    print("Verificando micrófono...")
    if recorder.test_microphone():
        print("✅ Micrófono disponible\n")
        
        # Mostrar dispositivos disponibles
        print("Dispositivos de audio disponibles:")
        devices = recorder.get_available_devices()
        for device in devices:
            print(f"  - {device['name']} ({device['channels']} canales)")
        
        # Grabar audio
        print("\n¡Prepárate para tocar una nota!")
        input("Presiona Enter para comenzar la grabación...")
        
        try:
            output_file = recorder.record(duration=3.0)
            print(f"\n✅ Grabación exitosa: {output_file}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("❌ No se puede acceder al micrófono")
        print("Verifica los permisos de micrófono en Configuración del Sistema")
