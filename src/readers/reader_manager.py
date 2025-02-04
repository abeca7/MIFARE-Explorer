# Import common utilities from the utils.common_imports module
import smartcard.System
import utils.APDU_commands as APDU
from utils.utilities import handle_apdu_response, toHexString
import utils.des_operations as des
from smartcard.Exceptions import NoCardException

# NFCReader class to manage the NFC reader connection and interactions
class NFCReader:
    def __init__(self):
        self.name = None
        self.reader = None
        self.connection = None
        self.initialize()

    def initialize(self):
        try:
            readers = smartcard.System.readers()
            if not readers:
                raise Exception("No NFC readers found")

            self.name = readers[0].name
            self.reader = readers[0]
        except Exception as e:
            print(f"Error initializing NFCReader: {e}")

    def connect(self):
        try:
            if not self.reader:
                raise Exception("Reader is not initialized")

            self.connection = self.reader.createConnection()
            self.connection.connect()

        except NoCardException:
            print("No card detected on the reader")
            return None
        except Exception as e:
            print(f"Error connecting to the NFC reader: {e}")
            return None

    def get_card_uid(connection):
        """
        Send an APDU command to retrieve the UID of the card.
        APDU Command: [0xFF, 0xCA, 0x00, 0x00, 0x00] requests the UID from the card.
        Returns the UID by processing the response using handle_apdu_response.
        """
        response, sw1, sw2 = connection.connection.transmit(APDU.GET_UID)
        return handle_apdu_response(sw1, sw2, response)

    def select_file(connection):
        """
        Send an APDU command to select a file (like a root directory on the card).
        APDU Command: [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00] selects the main file directory.
        Returns the result by processing the response using handle_apdu_response.
        """
        response, sw1, sw2 = connection.connection.transmit(APDU.SELECT_FILE)
        return handle_apdu_response(sw1, sw2, response)

    def get_atr(connection):
        """
        Retrieve the Answer to Reset (ATR) from the card.
        The ATR is a series of bytes sent from the card to the reader upon initialization.
        This function returns the ATR as a human-readable hex string using toHexString.
        """
        atr = connection.connection.getATR()
        return toHexString(atr)

    def get_version(connection):
        """
        Send an APDU command to retrieve the version of the card.
        If the card is a MIFARE DESFire card, it will handle multiple frames if necessary.
        Returns the version information and a flag indicating if it is a MIFARE DESFire card.
        """
        try:
            version_info = []
        
            # First frame
            response, sw1, sw2 = connection.connection.transmit(APDU.GET_VERSION)
            version_info.append(toHexString(response))
            # Handle multiple frames if SW1=0x91 and SW2=0xAF (More data available)
            while sw1 == 0x91 and sw2 == 0xAF:
                # Send APDU to request the next frame (90 AF 00 00 00)
                response, sw1, sw2 = connection.connection.transmit(APDU.NEXT_FRAME)
                version_info.append(toHexString(response))

            # Check if the card is a MIFARE DESFire card based on status words
            if sw1 == 0x91 and sw2 == 0x00:            
                return True, version_info  # Return version info and True for DESFire
            else:
                return False  # Return None and False if not DESFire

        except Exception as e:
            return False  # Return None and False in case of an error

    def authentication(connection, key, keyNumber, iv):
        """
        Send an APDU command to authenticate to a specific sector on the card.
        The key is provided as a hexadecimal string (e.g., "00 00 00 00 00 00 00 00").
        Returns the response from the card after authentication.
        """
        iv_bytes = bytes.fromhex(iv)
        key_bytes = bytes.fromhex(key)
        # Utilizar el keyNumber que se recibe como parametro
        response, sw1, sw2 = connection.connection.transmit(APDU.AUTHENTICATE)

        # Random number encrypted with the key sent by the card
        randomB = handle_apdu_response(sw1, sw2, response)

        # Decrypt the random number using the provided key
        print("Test before decrypt")
        decrypted_randomB, updated_iv = des.decrypt(randomB, key_bytes, iv_bytes)
        print(decrypted_randomB)
        decrypted_randomB_str = toHexString(decrypted_randomB)

        # Rotate left the dercypted random number
        rotatedB = decrypted_randomB_str[2:] + " " + decrypted_randomB_str[:2]

        # Random number created by the user // In this case the random number is fixed for testing purposes (00 00 00 00 00 00 00 00)
        randomA = "00 00 00 00 00 00 00 00"

        # Concatentate the random number created by the user with the rotated decrypted random number
        concatenated = randomA + rotatedB
        print("Concatenated: ", concatenated)

        # Encrypt the concatenated random numbers with the key
        encrypted_concatenated, updated_iv = des.encrypt(concatenated, key_bytes, updated_iv)
        encrypted_concatenated_str = toHexString(encrypted_concatenated)
        # Print the updated IV to use in DES Calculator to check
        print("Encrypted concatenated: ", encrypted_concatenated_str)

        # Send the encrypted concatenated random numbers to the card
        apdu_command = [0x90, 0xAF, 0x00, 0x00, 0x10] + encrypted_concatenated + [0x00]
        response, sw1, sw2 = connection.connection.transmit(apdu_command)
        encrypted_randomA = toHexString(response)
        randomA_decrypted, updated_iv = des.decrypt(encrypted_randomA, key_bytes, updated_iv)
        print("RandomA decrypted: ", randomA_decrypted)
        randomA_decrypted_str = toHexString(randomA_decrypted)
        print("RandomA decrypted str: ", randomA_decrypted_str)

        if sw1 == 0x91 and sw2 == 0x00:
            return True
        else:    
            return False
    
    def loadKey(connection, key):
        """
        Send an APDU command to load a key into the card.
        """
        key_bytes = bytes.fromhex(key)
        response, sw1, sw2 = connection.connection.transmit(APDU.LOADKEY + list(key_bytes))
        if sw1 == 0x90 and sw2 == 0x00:
            return True
        else:    
            return False
    
    def authentication_classic(connection, block_number, key_type):
        #block_number_byte = bytes.fromhex(block_number)
        if key_type == "A":
            key_type_byte = 0x60
        elif key_type == "B":
            key_type_byte = 0x61

        response, sw1, sw2 = connection.connection.transmit(APDU.AUTH_CLAS(block_number, key_type_byte))
        #return handle_apdu_response(sw1, sw2, response)
        if sw1 == 0x90 and sw2 == 0x00:
            return True
        else:    
            return False
    
    def read_binary(connection, block_number):
        response, sw1, sw2 = connection.connection.transmit(APDU.READ_BINARY(block_number))
        if sw1 == 0x90 and sw2 == 0x00:
            return response, True
        else:    
            return response, False
    
    def change_key(connection, block, keyA, keyB):

        # Calcular el bloque del sector trailer
        block_number = (block // 4) * 4 + 3
        sector = block // 4

        keyA_bytes = list(bytes.fromhex(keyA))  # "11 22 33 44 55 66" -> [0x11, 0x22, 0x33, 0x44, 0x55, 0x66]
        keyB_bytes = list(bytes.fromhex(keyB))  # "FF FF FF FF FF FF" -> [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        data = keyA_bytes + [0xFF, 0x07, 0x80, 0x69] + keyB_bytes
        response, sw1, sw2 = connection.connection.transmit(APDU.WRITE_BINARY(block_number, data))
        if sw1 == 0x90 and sw2 == 0x00:
            return sector, True
        else:    
            return sector, False
        
    def write_binary(connection, block_number, data):

        data = list(bytes.fromhex(data))  # "11 22 33 44 55 66" -> [0x11, 0x22, 0x33, 0x44, 0x55, 0x66]
        response, sw1, sw2 = connection.connection.transmit(APDU.WRITE_BINARY(block_number, data))
        if sw1 == 0x90 and sw2 == 0x00:
            return True
        else:    
            return False

    def all_blocks(connection):
        for i in range(0, 63):
            block_number = i
            block_info = connection.read_binary(block_number)
        return True
    

    def brute_force_attack(self, key_file_path, key_type):
        try:
            # Leer claves del archivo y limpiar las líneas
            with open(key_file_path, "r") as file:
                key_list = [line.strip() for line in file if line.strip() and not line.startswith("#")]

            # Iterar sobre todas las claves en la lista
            for key in key_list:
                formatted_key = " ".join(key[i:i+2] for i in range(0, len(key), 2))
                print(f"Trying key: {formatted_key}...")

                # Intentar cargar la clave en la tarjeta
                if not self.loadKey(formatted_key):
                    print(f"Failed to load key: {formatted_key}")
                    continue  # Ir a la siguiente clave si no se puede cargar
                
                for i in range(0, 63):
                    block_number_bytes = i
                    # Intentar autenticarse con el bloque
                    if self.authentication_classic(block_number_bytes, key_type):
                        print(f"Valid key found: {formatted_key}")
                        return formatted_key, block_number_bytes, True  # Detenerse y devolver la clave válida

            # Si no se encuentra ninguna clave válida
            print("No valid key found in the provided key list.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
        return False

