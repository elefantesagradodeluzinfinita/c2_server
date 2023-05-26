from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/audio_stream")
def audio_stream():
    return Response(stream_audio(), mimetype="audio/wav")

def stream_audio():
    # Lógica para obtener los datos de audio en tiempo real
    # Puedes adaptar esta función según tus necesidades
    while True:
        audio_data = get_audio_data()
        yield (b"--audio_stream\r\n"
               b"Content-Type: audio/wav\r\n\r\n" + audio_data + b"\r\n")

@socketio.on("audio_stream")
def handle_audio_stream(audio_data):
    emit("audio_stream", audio_data, namespace="/")

if __name__ == "__main__":
    socketio.run(app)