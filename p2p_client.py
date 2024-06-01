import socket
import threading
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import hashlib

# Gerar chaves RSA
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Funções de criptografia
def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_message(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted

# Funções para dividir e montar arquivos
def split_file(filepath, chunk_size=1024):
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk

def assemble_file(filename, chunks):
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk)

# Função para calcular checksum
def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

# Função para verificar e solicitar partes faltantes
def verify_and_request_missing_chunks(chunks, expected_checksums):
    received_checksums = [calculate_checksum(chunk) for chunk in chunks]
    missing_chunks = []
    for i, checksum in enumerate(expected_checksums):
        if i >= len(received_checksums) or received_checksums[i] != checksum:
            missing_chunks.append(i)
    return missing_chunks

# Funções de registro e obtenção de peers
def register_with_discovery_server(discovery_ip, discovery_port, local_ip, local_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((discovery_ip, discovery_port))
    client_socket.send(f"REGISTER:{local_ip}:{local_port}".encode('utf-8'))
    client_socket.close()

def get_peers_from_discovery_server(discovery_ip, discovery_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((discovery_ip, discovery_port))
    client_socket.send("GET_PEERS".encode('utf-8'))
    peers = client_socket.recv(1024).decode('utf-8').split(',')
    client_socket.close()
    return peers

# Funções de comunicação entre peers
def listen_for_connections(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("FILE:"):
                handle_file_reception(client_socket, message[5:])
            else:
                print(f"Mensagem recebida: {message}")
        except:
            break
    client_socket.close()

def handle_file_reception(client_socket, filename):
    print(f"Recebendo arquivo: {filename}")
    chunks = []
    expected_checksums = []
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        chunk, checksum = data[:-32], data[-32:].decode('utf-8')
        chunks.append(chunk)
        expected_checksums.append(checksum)
    missing_chunks = verify_and_request_missing_chunks(chunks, expected_checksums)
    # Aqui deve ser implementado o reenvio de partes faltantes
    assemble_file(filename, chunks)

if __name__ == "__main__":
    local_ip = '127.0.0.1'
    local_port = 9001
    discovery_ip = '127.0.0.1'
    discovery_port = 9000

    # Registrar nó no servidor de descoberta
    register_with_discovery_server(discovery_ip, discovery_port, local_ip, local_port)

    # Obter lista de peers
    peers = get_peers_from_discovery_server(discovery_ip, discovery_port)
    print(f"Peers conectados: {peers}")

    # Iniciar servidor P2P para ouvir conexões de outros peers
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_ip, local_port))
    server_socket.listen(5)
    threading.Thread(target=listen_for_connections, args=(server_socket,)).start()

    # Conectar a um peer e enviar uma mensagem (exemplo)
    if peers:
        peer_ip, peer_port = peers[0].split(':')
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_ip, int(peer_port)))
        peer_socket.send("Olá, Peer!".encode('utf-8'))
        peer_socket.close()
