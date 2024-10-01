import socket
import threading
import random
import string

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 65432

# Categorias do jogo
categories = ['Animal', 'País', 'Objeto']

# Lista de jogadores conectados
clients = []

def handle_client(conn, addr):
    print(f"Novo jogador conectado: {addr}")
    
    # Gera uma letra aleatória
    letter = random.choice(string.ascii_uppercase)
    conn.sendall(f"Letra: {letter}\nCategorias: {', '.join(categories)}".encode())
    
    # Recebe a resposta do jogador
    data = conn.recv(1024).decode().strip().split(',')
    print(f"Respostas recebidas de {addr}: {data}")
    
    # Aqui poderia haver a validação e cálculo da pontuação.
    conn.sendall(f"Respostas registradas! Aguarde os outros jogadores.".encode())
    
    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor rodando em {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
