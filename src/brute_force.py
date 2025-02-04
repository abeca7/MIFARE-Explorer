from PySide6.QtCore import QThread, Signal

class BruteForceThread(QThread):
    update_progress = Signal(int, int)  # Señal para actualizar el progreso
    finished = Signal(list, list, int, bool)  # Señal para el resultado final (clave A, clave B, sector, éxito)

    def __init__(self, key_file_path, loadKey, authentication_classic, sector=None):
        super().__init__()
        self.key_file_path = key_file_path
        self.loadKey = loadKey
        self.authentication_classic = authentication_classic
        self.sector = sector

    def run(self):
        try:
            # Leer claves del archivo
            with open(self.key_file_path, "r") as file:
                key_list = [line.strip() for line in file if line.strip() and not line.startswith("#")]

            # Determinar los bloques a probar
            if self.sector is None:
                sectors_to_test = range(16)  # Todos los sectores
            else:
                sectors_to_test = [self.sector]  # Solo el sector seleccionado

            total_attempts = len(key_list) * len(sectors_to_test) * 2  # Claves * Sectores * Tipos (A y B)
            current_attempt = 0
            found_keys_a = []
            found_keys_b = []
            for sector in sectors_to_test:
                block_number = (sector * 4) + 3  # Bloque trailer del sector
                found_key_a = None
                found_key_b = None

                for key in key_list:
                    formatted_key = " ".join(key[i:i+2] for i in range(0, len(key), 2))

                    if not self.loadKey(formatted_key):
                        continue  # Si la clave no se puede cargar, omitir

                    # Probar la clave con ambos tipos (A y B)
                    for key_type in ["A", "B"]:
                        current_attempt += 1
                        self.update_progress.emit(current_attempt, total_attempts)  # Emitir progreso

                        if self.authentication_classic(block_number, key_type):
                            if key_type == "A":
                                found_key_a = formatted_key
                                found_keys_a.append(formatted_key)
                            else:
                                found_key_b = formatted_key
                                found_keys_b.append(formatted_key)

                        # Si ambas claves se han encontrado para este sector, terminamos
                        if found_key_a and found_key_b:
                            break

                    if found_key_a and found_key_b:
                        break  # No seguir probando claves en este sector
                if self.sector is not None:
                    # Emitir resultado si al menos una clave fue encontrada
                    if found_key_a or found_key_b:
                        self.finished.emit([found_key_a], [found_key_b], sector, True)
                    else:
                        self.finished.emit([], [], sector, False)

            if self.sector is None:
                if found_keys_a or found_keys_b:
                    self.finished.emit(found_keys_a, found_keys_b, None, True)

        except Exception as e:
            print(f"Error in BruteForceThread: {e}")
            self.finished.emit(None, None, -1, False)
