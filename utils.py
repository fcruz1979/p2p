# utils.py

import socket
from port_lock import PortLock

def find_available_port(start_port, end_port):
    """ Encontra e reserva uma porta disponível entre start_port e end_port (inclusive). """
    for port in range(start_port, end_port + 1):
        lock = PortLock(port)
        if lock.acquire():
            try:
                # Tenta vincular à porta
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(("localhost", port))
                sock.listen(1)  # Escuta por conexões entrantes
                sock.close()
                return port
            except OSError:
                continue
            finally:
                lock.release()

    raise RuntimeError("Não foi possível encontrar uma porta disponível.")
