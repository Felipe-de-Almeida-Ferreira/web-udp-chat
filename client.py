import socket
#from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, request

app = Flask(__name__)

c = None
ip = None
local = input("Local/Remote|L/R: ")

def init_socket():
    global c, ip
    if not c:
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hostname = "DESKTOP-8C6B68Q" if local == 'L' else "127.0.0.1"
        ip = socket.gethostbyname(hostname)


@app.route("/", methods=["GET", "POST"])
def index():
    global c, ip

    init_socket()
    if request.method == "POST":
        mensagem_client = request.form.get("message")
        if mensagem_client:
            c.sendto(mensagem_client.encode('utf-8'), (ip, 8811))
    return render_template("index.html")

    '''mensagem_servidor = c.recvfrom(1024)[0].decode('utf-8')
    if mensagem_servidor == "close":
        break'''

    #print(mensagem_servidor)

def close_socket(exception=None):
    global c
    # Apenas fecha o socket se ele não estiver já fechado
    if c:
        print("Closing socket...")
        c.close()
        c = None  # Reseta o socket para garantir que ele não será usado novamente
        print("Client socket closed.")

if __name__ == "__main__":
    init_socket()
    app.run(debug=True)