import socket
import pyaudio

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

# Set up pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

# Stream audio from microphone to socket
while True:
    data = stream.read(1024)
    sock.sendall(data)

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
sock.close()