import socket
import threading
import random
import string
from PyDictionary import PyDictionary
from deep_translator import PonsTranslator

# Configurações do servidor
HOST = '25.1.48.60'
PORT = 65432

# Categorias do jogo
categories = ['Animal', 'País', 'Objeto']

# Inicializa o dicionário para validação
dictionary = PyDictionary()

# Lista de jogadores conectados
clients = []

def validate_word(word):
    """Verifica se a palavra existe usando um dicionário."""
    print(f"{word} antes do dictionary")
    if dictionary.meaning(word):
        print(f"{word} dentro do dictionary")
        return True # Se existir algum significado, a palavra é válida
    else:
        print(f"{word} depois do dictionary")
        return False

def handle_client(conn, addr):
    pontuacao = 0

    print(f"Novo jogador conectado: {addr}")
    
    # Gera uma letra aleatória
    letter = random.choice(string.ascii_uppercase)
    conn.sendall(f'=================================== Regras ===================================\n1- Escreva palavras com a letra sorteada\n2- Não colocar palavras compostas\n3- Não colocar palavras que possuem acento\n4- Separe as palavras por espaço e vírgula "Pato, Paris, Papel"\n6- Como não temos a checagem de categoria, por favor respeite as categorias\n------------------------------------------------------------------------------\n*** A PONTUAÇÃO SERÁ FEITA COM BASE NO TAMANHO DA PALAVRA ***\nLetra: {letter}\nCategorias: {', '.join(categories)}\n=============================================================================='.encode())
    
    # Recebe a resposta do jogador
    data = conn.recv(1024).decode().strip().split(',')
    print(f"Respostas recebidas de {addr}: {data}")
    
    # Validação das palavras
    feedback = []
    for i, word in enumerate(data):
        print(f"{word} antes do if")
        if word.strip().upper().startswith(letter.upper()) and validate_word(PonsTranslator(source='pt', target='en').translate(word.strip(), return_all=False)):
            feedback.append(f"'{word}' na categoria {categories[i]}: CORRETA")
            pontuacao += len(word.strip())
        else:
            feedback.append(f"'{word}' na categoria {categories[i]}: ERRADA")

    feedback.append(f"Sua pontuação total foi de {pontuacao} ponto(s)!!")

    # Envia feedback para o jogador
    conn.sendall("\n".join(feedback).encode())
    
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
