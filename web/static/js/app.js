// App.js - Lógica principal de la aplicación

const recorder = new AudioRecorder();
let currentFile = null;

// Elementos del DOM
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const recordBtn = document.getElementById('recordBtn');
const fileName = document.getElementById('fileName');
const loading = document.getElementById('loading');
const countdownDialog = document.getElementById('countdownDialog');
const countdownNumber = document.getElementById('countdownNumber');

// Event Listeners
uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        currentFile = file;
        fileName.textContent = `Archivo: ${file.name}`;

        // Configurar reproductor de audio
        const audioPlayer = document.getElementById('audioPlayer');
        const audioPlayerContainer = document.getElementById('audioPlayerContainer');
        const playBtn = document.getElementById('playBtn');

        audioPlayer.src = URL.createObjectURL(file);
        audioPlayerContainer.style.display = 'block';

        // Manejar botón de reproducción
        playBtn.onclick = () => {
            if (audioPlayer.paused) {
                audioPlayer.play();
                playBtn.textContent = '⏸️ Pausar Audio';
            } else {
                audioPlayer.pause();
                playBtn.textContent = '▶️ Reproducir Audio';
            }
        };

        // Resetear botón cuando termine
        audioPlayer.onended = () => {
            playBtn.textContent = '▶️ Reproducir Audio';
        };

        analyzeFile(file);
    }
});

recordBtn.addEventListener('click', startLiveRecording);

// Analizar archivo subido
async function analyzeFile(file) {
    showLoading(true);

    const formData = new FormData();
    formData.append('audio', file);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            displayResults(result);
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al analizar el archivo');
    } finally {
        showLoading(false);
    }
}

// Grabar en vivo
async function startLiveRecording() {
    // Mostrar cuenta regresiva
    showCountdown();

    await countdown(3);

    // Iniciar grabación
    countdownNumber.textContent = '🎤';
    countdownNumber.style.color = '#06ffa5';

    try {
        const audioBlob = await recorder.startRecording(3000);

        // Cerrar diálogo
        countdownDialog.style.display = 'none';
        showLoading(true);

        // Convertir a base64 y enviar
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = async () => {
            const base64Audio = reader.result.split(',')[1];

            try {
                const response = await fetch('/analyze-live', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ audio: base64Audio })
                });

                const result = await response.json();

                if (result.success) {
                    displayResults(result);
                } else {
                    alert(`Error: ${result.error}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al analizar la grabación');
            } finally {
                showLoading(false);
            }
        };
    } catch (error) {
        console.error('Error al grabar:', error);
        countdownDialog.style.display = 'none';
        alert('Error al grabar audio');
    }
}

// Mostrar cuenta regresiva
function showCountdown() {
    countdownDialog.style.display = 'flex';
    countdownNumber.textContent = '3';
    countdownNumber.style.color = '#ff6b9d';
}

// Cuenta regresiva
function countdown(seconds) {
    return new Promise((resolve) => {
        let count = seconds;
        const interval = setInterval(() => {
            count--;
            if (count > 0) {
                countdownNumber.textContent = count;
            } else {
                clearInterval(interval);
                resolve();
            }
        }, 1000);
    });
}

// Mostrar resultados
function displayResults(result) {
    if (!result.has_valid_signal) {
        // Sin señal válida
        document.querySelector('.note-text').textContent = '🔇';
        document.getElementById('frequency').textContent = 'No se detectó señal de audio válida';
        document.getElementById('cents').textContent = 'Toca una nota clara en tu instrumento';
        document.getElementById('status').textContent = '⚠️ Señal muy débil o solo ruido';
        document.getElementById('status').className = 'status-text flat';
        return;
    }

    // Mostrar nota
    document.querySelector('.note-text').textContent = result.note;

    // Mostrar frecuencia
    document.getElementById('frequency').textContent =
        `Frecuencia detectada: ${result.frequency} Hz (Nota exacta: ${result.exact_frequency} Hz)`;

    // Mostrar desviación
    const cents = result.cents;
    document.getElementById('cents').textContent = `Desviación: ${cents > 0 ? '+' : ''}${cents} cents`;

    // Mostrar estado de afinación
    const statusEl = document.getElementById('status');
    statusEl.textContent = result.tuning_status;

    if (Math.abs(cents) < 10) {
        statusEl.className = 'status-text in-tune';
    } else if (cents > 0) {
        statusEl.className = 'status-text sharp';
    } else {
        statusEl.className = 'status-text flat';
    }

    // Dibujar forma de onda si está disponible
    if (result.waveform && result.waveform.length > 0) {
        drawWaveform(result.waveform);
    }
}

// Dibujar forma de onda en canvas
function drawWaveform(waveformData) {
    const canvas = document.getElementById('waveform');
    const ctx = canvas.getContext('2d');

    // Limpiar canvas
    ctx.fillStyle = '#232946';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Configurar estilo
    ctx.strokeStyle = '#06ffa5';
    ctx.lineWidth = 2;

    // Normalizar datos
    const max = Math.max(...waveformData.map(Math.abs));
    const normalized = waveformData.map(v => v / max);

    // Dibujar
    ctx.beginPath();
    const step = canvas.width / normalized.length;
    const centerY = canvas.height / 2;

    normalized.forEach((value, i) => {
        const x = i * step;
        const y = centerY + (value * centerY * 0.8);

        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();
}

// Mostrar/ocultar loading
function showLoading(show) {
    loading.style.display = show ? 'flex' : 'none';
}
