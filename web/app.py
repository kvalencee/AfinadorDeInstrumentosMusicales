"""
Afinador Musical - Flask Web Application
Servidor web para análisis de audio de instrumentos musicales
"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import base64
from audio_analyzer import analyze_audio
import numpy as np

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analizar archivo de audio subido"""
    try:
        # Verificar que se subió un archivo
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No se encontró archivo de audio'}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionó ningún archivo'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Solo se permiten archivos WAV'}), 400
        
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analizar audio
        result = analyze_audio(filepath)
        
        # Limpiar archivo temporal
        os.remove(filepath)
        
        if result['success']:
            # Preparar respuesta - convertir numpy types a Python types
            # Incluir datos de forma de onda (muestreados para reducir tamaño)
            audio_data = result.get('audio_data', [])
            if len(audio_data) > 1000:
                # Submuestrear a 1000 puntos para el gráfico
                step = len(audio_data) // 1000
                waveform = audio_data[::step].tolist()
            else:
                waveform = audio_data.tolist() if hasattr(audio_data, 'tolist') else []
            
            response = {
                'success': True,
                'note': result['note_formatted'],
                'frequency': float(result['frequency']),
                'exact_frequency': float(result['exact_frequency']),
                'cents': float(result['cents']),
                'tuning_status': result['tuning_status'],
                'has_valid_signal': bool(result.get('has_valid_signal', True)),
                'signal_strength': float(result.get('signal_strength', 0)),
                'waveform': waveform[:1000]  # Máximo 1000 puntos
            }
            return jsonify(response)
        else:
            return jsonify({'success': False, 'error': result['error']}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/analyze-live', methods=['POST'])
def analyze_live():
    """Analizar audio grabado en vivo desde el navegador"""
    try:
        data = request.get_json()
        
        if not data or 'audio' not in data:
            return jsonify({'success': False, 'error': 'No se recibieron datos de audio'}), 400
        
        # Decodificar audio base64
        audio_data = base64.b64decode(data['audio'])
        
        # Guardar temporalmente
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.write(audio_data)
        temp_file.close()
        
        # Analizar
        result = analyze_audio(temp_file.name)
        
        # Limpiar
        os.remove(temp_file.name)
        
        if result['success']:
            response = {
                'success': True,
                'note': result['note_formatted'],
                'frequency': float(result['frequency']),
                'exact_frequency': float(result['exact_frequency']),
                'cents': float(result['cents']),
                'tuning_status': result['tuning_status'],
                'has_valid_signal': bool(result.get('has_valid_signal', True)),
                'signal_strength': float(result.get('signal_strength', 0))
            }
            return jsonify(response)
        else:
            return jsonify({'success': False, 'error': result['error']}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
