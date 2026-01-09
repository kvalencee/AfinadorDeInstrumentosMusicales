"""
Musical Instrument Tuner - GUI Application
Graphical interface for uploading audio files and detecting musical notes
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import sys
import threading
from audio_analyzer import analyze_audio
from live_recorder import LiveRecorder
from custom_button import CustomButton


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class TunerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Afinador de Instrumentos Musicales")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        
        # Current analysis result
        self.current_result = None
        
        # Live recorder
        self.recorder = LiveRecorder()
        self.is_recording = False
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Create the user interface"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🎵 Afinador de Instrumentos Musicales 🎵",
            font=('Arial', 24, 'bold'),
            bg='#1a1a2e',
            fg='#00d4ff'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Detecta notas musicales usando análisis FFT",
            font=('Arial', 12),
            bg='#1a1a2e',
            fg='#a0a0a0'
        )
        subtitle_label.pack()
        
        # File selection frame
        file_frame = tk.Frame(self.root, bg='#1a1a2e')
        file_frame.pack(pady=20)
        
        self.file_label = tk.Label(
            file_frame,
            text="Ningún archivo seleccionado",
            font=('Arial', 11),
            bg='#1a1a2e',
            fg='#ffffff'
        )
        self.file_label.pack(pady=10)
        
        button_frame = tk.Frame(file_frame, bg='#1a1a2e')
        button_frame.pack()
        
        self.upload_button = CustomButton(
            button_frame,
            text="📁 Seleccionar Archivo de Audio",
            command=self.upload_file,
            font=('Arial', 12, 'bold'),
            bg='#4a90e2',
            fg='#ffffff',
            activebackground='#357abd',
            activeforeground='#ffffff',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        self.record_button = CustomButton(
            button_frame,
            text="🎤 Grabar en Vivo",
            command=self.start_live_recording,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='#ffffff',
            activebackground='#c0392b',
            activeforeground='#ffffff',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = CustomButton(
            button_frame,
            text="🔍 Analizar",
            command=self.analyze_file,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='#ffffff',
            activebackground='#229954',
            activeforeground='#ffffff',
            padx=20,
            pady=10,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, borderwidth=2)
        results_frame.pack(pady=20, padx=40, fill=tk.BOTH)
        
        results_title = tk.Label(
            results_frame,
            text="Resultados del Análisis",
            font=('Arial', 16, 'bold'),
            bg='#16213e',
            fg='#00d4ff'
        )
        results_title.pack(pady=10)
        
        # Note display (large)
        self.note_label = tk.Label(
            results_frame,
            text="--",
            font=('Arial', 72, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        self.note_label.pack(pady=10)
        
        # Frequency and deviation
        info_frame = tk.Frame(results_frame, bg='#16213e')
        info_frame.pack(pady=10)
        
        self.freq_label = tk.Label(
            info_frame,
            text="Frecuencia: -- Hz",
            font=('Arial', 14),
            bg='#16213e',
            fg='#a0a0a0'
        )
        self.freq_label.pack()
        
        self.cents_label = tk.Label(
            info_frame,
            text="Desviación: -- cents",
            font=('Arial', 14),
            bg='#16213e',
            fg='#a0a0a0'
        )
        self.cents_label.pack()
        
        self.status_label = tk.Label(
            info_frame,
            text="",
            font=('Arial', 16, 'bold'),
            bg='#16213e',
            fg='#16c79a'
        )
        self.status_label.pack(pady=5)
        
        # Visualization frame
        viz_frame = tk.Frame(self.root, bg='#1a1a2e')
        viz_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure for waveform
        self.figure = Figure(figsize=(8, 2.5), facecolor='#16213e')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#1a1a2e')
        self.ax.set_title('Forma de Onda del Audio', color='#00d4ff', fontsize=12)
        self.ax.set_xlabel('Tiempo (s)', color='#a0a0a0')
        self.ax.set_ylabel('Amplitud', color='#a0a0a0')
        self.ax.tick_params(colors='#a0a0a0')
        self.ax.grid(True, alpha=0.2, color='#00d4ff')
        
        self.canvas = FigureCanvasTkAgg(self.figure, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="Soporta archivos WAV • Proyecto 1 - ESCOM",
            font=('Arial', 9),
            bg='#1a1a2e',
            fg='#606060'
        )
        footer_label.pack(pady=10)
    
    def upload_file(self):
        """Handle file upload"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[
                ("Archivos WAV", "*.wav"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"Archivo: {filename}")
            self.analyze_button.config(state=tk.NORMAL)
            
            # Clear previous results
            self.clear_results()
    
    def analyze_file(self):
        """Analyze the selected audio file"""
        if not hasattr(self, 'current_file'):
            messagebox.showerror("Error", "Por favor selecciona un archivo primero")
            return
        
        # Show processing message
        self.note_label.config(text="⏳", fg='#ffaa00')
        self.root.update()
        
        try:
            # Analyze audio
            result = analyze_audio(self.current_file)
            
            if result['success']:
                self.current_result = result
                self.display_results(result)
            else:
                messagebox.showerror("Error de Análisis", f"Error: {result['error']}")
                self.clear_results()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el archivo: {str(e)}")
            self.clear_results()
    
    def display_results(self, result):
        """Display analysis results"""
        
        # Check if we have a valid signal
        if not result.get('has_valid_signal', True):
            # No valid signal detected
            self.note_label.config(text="🔇", fg='#ff4757')
            self.freq_label.config(
                text=f"No se detectó señal de audio válida (RMS: {result.get('signal_strength', 0):.4f})"
            )
            self.cents_label.config(
                text="Toca una nota clara en tu instrumento",
                fg='#ffaa00'
            )
            self.status_label.config(
                text="⚠️ Señal muy débil o solo ruido",
                fg='#ff4757'
            )
            
            # Still plot the waveform to show what was captured
            self.plot_waveform(result['audio_data'], result['sample_rate'])
            return
        
        # Display note
        self.note_label.config(text=result['note_formatted'], fg='#00d4ff')
        
        # Display frequency
        self.freq_label.config(
            text=f"Frecuencia detectada: {result['frequency']:.2f} Hz "
                 f"(Nota exacta: {result['exact_frequency']:.2f} Hz)"
        )
        
        # Display cents deviation
        cents = result['cents']
        cents_text = f"Desviación: {cents:+.1f} cents"
        
        if abs(cents) < 10:
            cents_color = '#16c79a'  # Green - in tune
        elif abs(cents) < 30:
            cents_color = '#ffaa00'  # Orange - slightly off
        else:
            cents_color = '#ff4757'  # Red - out of tune
        
        self.cents_label.config(text=cents_text, fg=cents_color)
        
        # Display tuning status
        self.status_label.config(text=result['tuning_status'])
        
        if "✓" in result['tuning_status']:
            self.status_label.config(fg='#16c79a')
        elif "Agudo" in result['tuning_status']:
            self.status_label.config(fg='#ffaa00')
        else:
            self.status_label.config(fg='#ff4757')
        
        # Plot waveform
        self.plot_waveform(result['audio_data'], result['sample_rate'])
    
    def plot_waveform(self, audio_data, sample_rate):
        """Plot audio waveform"""
        self.ax.clear()
        
        # Create time axis
        duration = len(audio_data) / sample_rate
        
        # Show only first 0.05 seconds to see actual wave oscillations
        # This makes the sine waves visible instead of a solid block
        display_duration = min(0.05, duration)  # 50 milliseconds
        num_samples_to_show = int(display_duration * sample_rate)
        
        audio_to_plot = audio_data[:num_samples_to_show]
        time = np.linspace(0, display_duration, num_samples_to_show)
        
        # Plot waveform
        self.ax.plot(time, audio_to_plot, color='#00d4ff', linewidth=1.5)
        self.ax.set_facecolor('#1a1a2e')
        self.ax.set_title('Forma de Onda del Audio (primeros 50ms)', color='#00d4ff', fontsize=12)
        self.ax.set_xlabel('Tiempo (s)', color='#a0a0a0')
        self.ax.set_ylabel('Amplitud', color='#a0a0a0')
        self.ax.tick_params(colors='#a0a0a0')
        self.ax.grid(True, alpha=0.2, color='#00d4ff')
        
        # Add note about what we're showing
        self.ax.text(0.98, 0.95, f'Mostrando {display_duration*1000:.0f}ms de {duration:.2f}s totales',
                    transform=self.ax.transAxes,
                    ha='right', va='top',
                    color='#a0a0a0',
                    fontsize=8,
                    bbox=dict(boxstyle='round', facecolor='#16213e', alpha=0.8, edgecolor='none'))
        
        # Update canvas
        self.canvas.draw()
    
    def clear_results(self):
        """Clear all results"""
        self.note_label.config(text="--", fg='#ffffff')
        self.freq_label.config(text="Frecuencia: -- Hz")
        self.cents_label.config(text="Desviación: -- cents", fg='#a0a0a0')
        self.status_label.config(text="")
        
        # Clear plot
        self.ax.clear()
        self.ax.set_facecolor('#1a1a2e')
        self.ax.set_title('Forma de Onda del Audio', color='#00d4ff', fontsize=12)
        self.ax.set_xlabel('Tiempo (s)', color='#a0a0a0')
        self.ax.set_ylabel('Amplitud', color='#a0a0a0')
        self.ax.tick_params(colors='#a0a0a0')
        self.ax.grid(True, alpha=0.2, color='#00d4ff')
        self.canvas.draw()
    
    def start_live_recording(self):
        """Start live audio recording"""
        if self.is_recording:
            messagebox.showwarning("Grabando", "Ya hay una grabación en proceso")
            return
        
        # Test microphone first
        if not self.recorder.test_microphone():
            messagebox.showerror(
                "Error de Micrófono",
                "No se puede acceder al micrófono.\n\n"
                "Verifica que:\n"
                "1. Tu micrófono esté conectado\n"
                "2. La aplicación tenga permisos de micrófono\n"
                "3. Ninguna otra aplicación esté usando el micrófono"
            )
            return
        
        # Show countdown dialog
        self.show_countdown_and_record()
    
    def show_countdown_and_record(self):
        """Show countdown dialog and start recording"""
        # Create countdown dialog
        countdown_dialog = tk.Toplevel(self.root)
        countdown_dialog.title("Preparando Grabación")
        countdown_dialog.geometry("400x250")
        countdown_dialog.configure(bg='#1a1a2e')
        countdown_dialog.resizable(False, False)
        
        # Center the dialog
        countdown_dialog.transient(self.root)
        countdown_dialog.grab_set()
        
        # Countdown label
        countdown_label = tk.Label(
            countdown_dialog,
            text="Prepárate para tocar...",
            font=('Arial', 16, 'bold'),
            bg='#1a1a2e',
            fg='#00d4ff'
        )
        countdown_label.pack(pady=20)
        
        # Number display
        number_label = tk.Label(
            countdown_dialog,
            text="3",
            font=('Arial', 72, 'bold'),
            bg='#1a1a2e',
            fg='#ff6b6b'
        )
        number_label.pack(pady=10)
        
        # Instruction label
        instruction_label = tk.Label(
            countdown_dialog,
            text="Toca una nota clara en tu instrumento",
            font=('Arial', 11),
            bg='#1a1a2e',
            fg='#a0a0a0'
        )
        instruction_label.pack(pady=10)
        
        # Countdown sequence
        def countdown(count):
            if count > 0:
                number_label.config(text=str(count))
                countdown_dialog.after(1000, lambda: countdown(count - 1))
            else:
                number_label.config(text="🎤", fg='#16c79a')
                countdown_label.config(text="¡Grabando!")
                instruction_label.config(text="Tocando nota...")
                
                # Start recording in a separate thread
                threading.Thread(target=self.record_audio, args=(countdown_dialog,), daemon=True).start()
        
        # Start countdown
        countdown_dialog.after(500, lambda: countdown(3))
    
    def record_audio(self, dialog):
        """Record audio in a separate thread"""
        self.is_recording = True
        
        try:
            # Record audio (3 seconds)
            output_file = self.recorder.record(duration=3.0)
            
            # Close countdown dialog
            dialog.destroy()
            
            # Set as current file and analyze
            self.current_file = output_file
            self.file_label.config(text=f"Archivo: Grabación en vivo")
            
            # Analyze automatically
            self.root.after(100, self.analyze_file)
            
        except Exception as e:
            dialog.destroy()
            messagebox.showerror(
                "Error de Grabación",
                f"No se pudo grabar el audio:\n{str(e)}"
            )
        
        finally:
            self.is_recording = False


def main():
    root = tk.Tk()
    app = TunerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
