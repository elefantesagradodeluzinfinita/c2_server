import logging
import pyaudio
import wave
import requests
import api
from flask import Flask, request, Response, stream_with_context
import threading

app = Flask(__name__)

# Ruta principal
@app.route("/")
def main():
    logging.info("Se ejecutó la función 'main'")
    return api.get_main()

@app.route('/stream_audio')
def stream_audio():
    CHUNK_SIZE = 1024
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    def generate():
        while True:
            data = stream.read(CHUNK_SIZE)
            yield data

    return Response(generate(), mimetype='audio/x-wav')

# Ruta para reproducir el archivo "attack.wav"
@app.route("/play_attack", methods=['GET'])
def play_attack():
    logging.info("Reproduciendo el archivo 'attack.wav'")
    threading.Thread(target=play_audio).start()
    return "Reproduciendo 'attack.wav'"

def play_audio():
    # Configuración del archivo de audio
    audio_file = "attack.wav"
    chunk = 1024

    # Inicializar PyAudio
    p = pyaudio.PyAudio()

    # Abrir el archivo de audio
    wf = wave.open(audio_file, 'rb')

    # Abrir el stream de reproducción
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Leer y reproducir el audio en bloques
    data = wf.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    # Cerrar los streams y terminar PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(9000))