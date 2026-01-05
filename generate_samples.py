"""
Generate sample audio files for testing the tuner
Creates WAV files with pure tones at specific musical note frequencies
"""

import numpy as np
from scipy.io import wavfile
import os

def generate_tone(frequency, duration=2.0, sample_rate=44100, amplitude=0.5):
    """
    Generate a pure tone at a specific frequency
    
    Args:
        frequency (float): Frequency in Hz
        duration (float): Duration in seconds
        sample_rate (int): Sample rate in Hz
        amplitude (float): Amplitude (0.0 to 1.0)
        
    Returns:
        numpy.array: Audio data
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    tone = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit PCM
    tone_int16 = np.int16(tone * 32767)
    
    return tone_int16


def create_sample_files():
    """Create sample audio files for testing"""
    
    # Create samples directory
    samples_dir = "samples"
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
    
    # Define test notes with their frequencies
    test_notes = {
        'A4_440Hz': 440.00,      # Standard tuning reference
        'E2_82Hz_guitar': 82.41,  # Low E string on guitar
        'C4_262Hz_middle_c': 261.63,  # Middle C on piano
        'G3_196Hz_violin': 196.00,    # G string on violin
        'A4_445Hz_sharp': 445.00,     # Slightly sharp A4 (about +20 cents)
        'A4_435Hz_flat': 435.00,      # Slightly flat A4 (about -20 cents)
    }
    
    print("Generando archivos de audio de prueba...")
    print("-" * 60)
    
    for name, freq in test_notes.items():
        filename = os.path.join(samples_dir, f"{name}.wav")
        tone = generate_tone(freq, duration=2.0)
        wavfile.write(filename, 44100, tone)
        print(f"✓ Creado: {filename} ({freq:.2f} Hz)")
    
    print("-" * 60)
    print(f"✓ {len(test_notes)} archivos de prueba creados en '{samples_dir}/'")
    print("\nPuedes usar estos archivos para probar el afinador:")
    print("  python tuner_gui.py")


if __name__ == "__main__":
    create_sample_files()
