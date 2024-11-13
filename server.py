import socket
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def configure_socket():
    local = input("Local/Remote|L/R: ")

    hostname = "DESKTOP-8C6B68Q" if local == 'L' else "127.0.0.1"
    ip = socket.gethostbyname(hostname)
    s.bind((ip, 8811))  # Bind only once when starting the server

configure_socket()

def receive_messages():
    while True:
        try:
            message, address = s.recvfrom(1024)
            message_client = message.decode('utf-8')

            if message_client == "close":
                s.sendto("close".encode('utf-8'), address)
                print("CONEXÃO ENCERRADA")
                break    

            print(message_client)
            socketio.emit('new_message', {'message': message_client})

        except Exception as e:
            print(f"Error: {e}")
            break
    s.close()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(receive_messages)

if __name__ == "__main__":
    socketio.run(app, debug=False)
