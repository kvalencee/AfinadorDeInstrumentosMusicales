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
from audio_analyzer import analyze_audio


class TunerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Afinador de Instrumentos Musicales")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        
        # Current analysis result
        self.current_result = None
        
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
        
        self.upload_button = tk.Button(
            button_frame,
            text="📁 Seleccionar Archivo de Audio",
            command=self.upload_file,
            font=('Arial', 12, 'bold'),
            bg='#00d4ff',
            fg='#1a1a2e',
            activebackground='#00a8cc',
            padx=20,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = tk.Button(
            button_frame,
            text="🔍 Analizar",
            command=self.analyze_file,
            font=('Arial', 12, 'bold'),
            bg='#16c79a',
            fg='#1a1a2e',
            activebackground='#11a67f',
            padx=20,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT,
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


def main():
    root = tk.Tk()
    app = TunerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
