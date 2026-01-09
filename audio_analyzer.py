"""
Audio Analyzer Module
Handles audio file loading, FFT analysis, and note detection
"""

import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import wave
from note_frequencies import get_note_from_frequency, format_note_name


def load_audio(file_path):
    """
    Load audio file and return audio data with sample rate
    
    Args:
        file_path (str): Path to audio file
        
    Returns:
        tuple: (audio_data, sample_rate)
    """
    try:
        # Try to load as WAV file
        sample_rate, audio_data = wavfile.read(file_path)
        
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalize to float
        if audio_data.dtype == np.int16:
            audio_data = audio_data.astype(np.float32) / 32768.0
        elif audio_data.dtype == np.int32:
            audio_data = audio_data.astype(np.float32) / 2147483648.0
        
        return audio_data, sample_rate
    
    except Exception as e:
        raise Exception(f"Error loading audio file: {str(e)}")


def get_fundamental_frequency(audio_data, sample_rate, window_size=None):
    """
    Extract fundamental frequency using FFT
    
    Args:
        audio_data (numpy.array): Audio signal data
        sample_rate (int): Sample rate in Hz
        window_size (int): Size of analysis window (default: use full signal)
        
    Returns:
        tuple: (fundamental_frequency in Hz, signal_strength, is_valid_signal)
    """
    # Check if there's enough signal amplitude
    # RMS (Root Mean Square) gives us the average signal strength
    rms = np.sqrt(np.mean(audio_data**2))
    
    # Minimum threshold for a valid signal (adjust based on testing)
    # 0.01 means at least 1% of full scale
    MIN_RMS_THRESHOLD = 0.01
    
    if rms < MIN_RMS_THRESHOLD:
        # Signal too weak - likely silence or just noise
        return 0.0, rms, False
    
    # Use a window of the signal for analysis
    if window_size is None:
        window_size = len(audio_data)
    
    # Take the middle portion of the audio for more stable results
    start_idx = max(0, len(audio_data) // 2 - window_size // 2)
    end_idx = min(len(audio_data), start_idx + window_size)
    windowed_data = audio_data[start_idx:end_idx]
    
    # Apply Hamming window to reduce spectral leakage
    window = np.hamming(len(windowed_data))
    windowed_data = windowed_data * window
    
    # Compute FFT
    fft_data = fft(windowed_data)
    fft_freqs = fftfreq(len(windowed_data), 1/sample_rate)
    
    # Only consider positive frequencies
    positive_freqs = fft_freqs[:len(fft_freqs)//2]
    magnitude = np.abs(fft_data[:len(fft_data)//2])
    
    # Find the peak frequency (fundamental)
    # Ignore very low frequencies (below 20 Hz) which are likely noise
    min_freq_idx = np.argmax(positive_freqs > 20)
    max_freq_idx = np.argmax(positive_freqs > 5000)  # Ignore above 5kHz for fundamental
    
    if max_freq_idx == 0:
        max_freq_idx = len(positive_freqs)
    
    search_range = magnitude[min_freq_idx:max_freq_idx]
    search_freqs = positive_freqs[min_freq_idx:max_freq_idx]
    
    if len(search_range) == 0:
        return 0.0, rms, False
    
    peak_idx = np.argmax(search_range)
    fundamental_freq = search_freqs[peak_idx]
    peak_magnitude = search_range[peak_idx]
    
    # Calculate Signal-to-Noise Ratio (SNR)
    # Compare peak magnitude to average magnitude
    avg_magnitude = np.mean(search_range)
    snr = peak_magnitude / (avg_magnitude + 1e-10)  # Avoid division by zero
    
    # Require a clear peak (SNR > 3 means peak is at least 3x stronger than average)
    MIN_SNR = 3.0
    
    if snr < MIN_SNR:
        # No clear fundamental frequency - likely just noise
        return 0.0, rms, False
    
    return fundamental_freq, rms, True


def analyze_audio(file_path):
    """
    Complete audio analysis: load file, detect frequency, identify note
    
    Args:
        file_path (str): Path to audio file
        
    Returns:
        dict: Analysis results containing:
            - 'frequency': Detected fundamental frequency
            - 'note': Closest musical note
            - 'exact_frequency': Exact frequency of the note
            - 'cents': Deviation in cents
            - 'note_formatted': Formatted note name
            - 'sample_rate': Audio sample rate
            - 'duration': Audio duration in seconds
            - 'audio_data': Raw audio data for visualization
            - 'signal_strength': RMS amplitude of the signal
            - 'has_valid_signal': Whether a valid musical signal was detected
    """
    try:
        # Load audio
        audio_data, sample_rate = load_audio(file_path)
        duration = len(audio_data) / sample_rate
        
        # Get fundamental frequency with signal validation
        fundamental_freq, signal_strength, has_valid_signal = get_fundamental_frequency(audio_data, sample_rate)
        
        # Check if we have a valid signal
        if not has_valid_signal:
            return {
                'frequency': 0.0,
                'note': 'N/A',
                'exact_frequency': 0.0,
                'cents': 0.0,
                'note_formatted': 'Sin señal',
                'tuning_status': 'No se detectó señal de audio válida',
                'sample_rate': sample_rate,
                'duration': duration,
                'audio_data': audio_data,
                'signal_strength': signal_strength,
                'has_valid_signal': False,
                'success': True,
                'error': None
            }
        
        # Identify note
        note, exact_freq, cents = get_note_from_frequency(fundamental_freq)
        note_formatted = format_note_name(note)
        
        # Determine if in tune (within ±10 cents is considered good)
        if abs(cents) < 10:
            tuning_status = "En tono ✓"
        elif cents > 0:
            tuning_status = "Agudo (sostenido)"
        else:
            tuning_status = "Grave (bemol)"
        
        return {
            'frequency': fundamental_freq,
            'note': note,
            'exact_frequency': exact_freq,
            'cents': cents,
            'note_formatted': note_formatted,
            'tuning_status': tuning_status,
            'sample_rate': sample_rate,
            'duration': duration,
            'audio_data': audio_data,
            'signal_strength': signal_strength,
            'has_valid_signal': True,
            'success': True,
            'error': None
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the analyzer
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Analyzing: {file_path}")
        print("-" * 60)
        
        result = analyze_audio(file_path)
        
        if result['success']:
            print(f"Detected Frequency: {result['frequency']:.2f} Hz")
            print(f"Closest Note: {result['note_formatted']}")
            print(f"Exact Frequency: {result['exact_frequency']:.2f} Hz")
            print(f"Deviation: {result['cents']:+.1f} cents")
            print(f"Status: {result['tuning_status']}")
            print(f"Duration: {result['duration']:.2f} seconds")
        else:
            print(f"Error: {result['error']}")
    else:
        print("Usage: python audio_analyzer.py <audio_file.wav>")
