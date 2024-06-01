# port_lock.py

import os
import time

class PortLock:
    def __init__(self, port):
        self.lockfile = f".port_lock_{port}"

    def acquire(self):
        try:
            # Tenta criar o arquivo de bloqueio
            with open(self.lockfile, 'x'):
                pass  # Arquivo criado com sucesso, porta está disponível
            return True
        except FileExistsError:
            return False

    def release(self):
        try:
            os.remove(self.lockfile)
        except FileNotFoundError:
            pass  # Caso o arquivo não exista, não há necessidade de removê-lo
