import socket
import threading

# Lista de nós conectados
peers = []

def handle_peer(client_socket):
    global peers
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message.startswith("REGISTER:"):
                    peer_info = message.split("REGISTER:")[1]
                    peers.append(peer_info)
                    print(f"Peer registrado: {peer_info}")
                elif message == "GET_PEERS":
                    client_socket.send(",".join(peers).encode('utf-8'))
                else:
                    break
        except:
            break
    client_socket.close()

def start_discovery_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Servidor de descoberta iniciado em {ip}:{port}")
    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_peer, args=(client_socket,)).start()

if __name__ == "__main__":
    start_discovery_server('127.0.0.1', 9000)
