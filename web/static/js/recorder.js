// Recorder.js - Web Audio API para grabación en vivo con conversión a WAV

class AudioRecorder {
    constructor() {
        this.audioContext = null;
        this.stream = null;
        this.source = null;
        this.processor = null;
        this.audioData = [];
    }

    async requestPermission() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            return true;
        } catch (error) {
            console.error('Error al acceder al micrófono:', error);
            alert('No se pudo acceder al micrófono. Verifica los permisos del navegador.');
            return false;
        }
    }

    async startRecording(duration = 3000) {
        if (!this.stream) {
            const hasPermission = await this.requestPermission();
            if (!hasPermission) return null;
        }

        return new Promise((resolve, reject) => {
            this.audioData = [];

            // Crear contexto de audio
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.source = this.audioContext.createMediaStreamSource(this.stream);

            // Crear procesador de audio
            const bufferSize = 4096;
            this.processor = this.audioContext.createScriptProcessor(bufferSize, 1, 1);

            this.processor.onaudioprocess = (e) => {
                const inputData = e.inputBuffer.getChannelData(0);
                this.audioData.push(new Float32Array(inputData));
            };

            this.source.connect(this.processor);
            this.processor.connect(this.audioContext.destination);

            // Detener después de la duración especificada
            setTimeout(() => {
                this.stopRecording();
                const wavBlob = this.exportWAV();
                resolve(wavBlob);
            }, duration);
        });
    }

    stopRecording() {
        if (this.processor) {
            this.processor.disconnect();
            this.processor = null;
        }
        if (this.source) {
            this.source.disconnect();
            this.source = null;
        }
    }

    exportWAV() {
        const sampleRate = this.audioContext.sampleRate;
        const numChannels = 1;

        // Combinar todos los buffers
        let totalLength = 0;
        for (let i = 0; i < this.audioData.length; i++) {
            totalLength += this.audioData[i].length;
        }

        const samples = new Float32Array(totalLength);
        let offset = 0;
        for (let i = 0; i < this.audioData.length; i++) {
            samples.set(this.audioData[i], offset);
            offset += this.audioData[i].length;
        }

        // Convertir a WAV
        const wavBuffer = this.encodeWAV(samples, sampleRate, numChannels);
        return new Blob([wavBuffer], { type: 'audio/wav' });
    }

    encodeWAV(samples, sampleRate, numChannels) {
        const bytesPerSample = 2; // 16-bit
        const blockAlign = numChannels * bytesPerSample;
        const byteRate = sampleRate * blockAlign;
        const dataSize = samples.length * bytesPerSample;

        const buffer = new ArrayBuffer(44 + dataSize);
        const view = new DataView(buffer);

        // WAV header
        this.writeString(view, 0, 'RIFF');
        view.setUint32(4, 36 + dataSize, true);
        this.writeString(view, 8, 'WAVE');
        this.writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true); // fmt chunk size
        view.setUint16(20, 1, true); // PCM format
        view.setUint16(22, numChannels, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, byteRate, true);
        view.setUint16(32, blockAlign, true);
        view.setUint16(34, 16, true); // bits per sample
        this.writeString(view, 36, 'data');
        view.setUint32(40, dataSize, true);

        // Escribir datos de audio (convertir float a int16)
        let offset = 44;
        for (let i = 0; i < samples.length; i++) {
            const sample = Math.max(-1, Math.min(1, samples[i]));
            view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
            offset += 2;
        }

        return buffer;
    }

    writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }

    cleanup() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
    }
}
