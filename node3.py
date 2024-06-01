# node3.py

from utils import find_available_port

if __name__ == "__main__":
    # Defina manualmente a porta para node3
    port = 8020

    # Encontre uma porta disponível próxima à porta definida
    actual_port = find_available_port(port, port + 10)
    print(f"Node 3: Porta disponível encontrada: {actual_port}")

    # Resto do código do node3.py
    # Coloque aqui o restante do código do node3.py que você já tem
