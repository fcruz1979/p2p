# node2.py

from utils import find_available_port

if __name__ == "__main__":
    # Defina manualmente a porta para node2
    port = 8012

    # Encontre uma porta disponível próxima à porta definida
    actual_port = find_available_port(port, port + 10)
    print(f"Node 2: Porta disponível encontrada: {actual_port}")

    # Resto do código do node2.py
    # Coloque aqui o restante do código do node2.py que você já tem
