import sys
import smartcard.System
from smartcard.util import toHexString
from readers.reader_manager import NFCReader
from dictionary.create_dictionary import create_atr_dictionary
from dictionary.search_atr import search_atr
from cards.DesFire import desfire_utils

key_list_path = "utils/keys.txt"
dict = create_atr_dictionary()
key_clas = "FF FF FF FF FF FF"
key_des = "00 00 00 00 00 00 00 00"
iv=b'\x00\x00\x00\x00\x00\x00\x00\x00'
keyNumber = "A"
sector = 0x00
block_number_test = 0x03

def main():
    print("Starting NFC Reader program...")
    try:
        nfc_reader = NFCReader()
        nfc_reader.connect()

        if not nfc_reader:
            raise Exception("Failed to connect to the NFC reader")
        
        uid = nfc_reader.get_card_uid()
        #uid_length = len(uid)

        atr = nfc_reader.get_atr()
        atr_finded = search_atr(dict, atr)
        card_type = atr_finded['card_type']
        description = ' | '.join(atr_finded['description'])
        
        if (card_type == "CLASSIC"):
            print("MIFARE Classic")
            # Hacer un doble check comprobando que el comando get_version le da error  --> En caso de error mover a Unknown
            if(nfc_reader.get_version() == True):
                card_type = "Unknown"
                return card_type
            # Revisar bloque de memoria +16 y comprobar la SW que devuelve, para 1k debería ser bloque no encontrado
            # para 4k debería devolver SW de que no te has autenticado
            if(len(uid) == 4):
                card_version = "1K"
            elif(len(uid) == 7):
                card_version = "4K"

            # Authentication communication
            load_key_response = nfc_reader.loadKey(key_clas)
            if(load_key_response == False):
                print("Error loading the key")
                return
            authentication = nfc_reader.authentication_classic(sector, keyNumber)
            #write_response = nfc_reader.write_binary(block_number_test, keyA="FF FF FF FF FF FF", keyB="FF FF FF FF FF FF")
            #print(write_response)
            #bruteforce = nfc_reader.brute_force_attack(key_list_path, keyNumber)

            for i in range(0, 63):
                block_number = i
                # Revisar enviar keyNumber a enviar al authenticate_classic
                authentication = nfc_reader.authentication_classic(block_number, keyNumber)
                if(authentication == False):
                    print("Error authenticating")
                    return
                block_info, auxx = nfc_reader.read_binary(block_number)
                print(f"Block {block_number}: {toHexString(block_info)}")
            # Hacer un bruteforce attack
            # Añadir opción para cambiar la clave en caso de autenticarse
            # Hacer un bruteforce attack a la clave
        elif (card_type == "DESFIRE"):
            print("MIFARE DESFire")
            # Ejecutar el get_version para conseguir la mayor información posible de la tarjeta
            flag, version_info = nfc_reader.get_version()
            if(flag == False):
                card_type = "Unknown"
                return card_type

            # Parsear la información de version_info para la app visual
            vendor, type, storage_size, protocol, hard_version, soft_version, card_version = desfire_utils.get_parsed_info(version_info)
            # Modificar esto para que se muestre en la app visual
            print(f"Vendor: {vendor}")
            print(f"Type: {type}")
            print(f"Storage Size: {storage_size}")
            print(f"Protocol: {protocol}")
            print(f"Hardware Version: {hard_version}")
            print(f"Software Version: {soft_version}")
            print(f"Card Version: {card_version}")

            # Authentication communication (REFORMULAR EL COMENTARIO)
            authentication = nfc_reader.authentication(key_des, keyNumber, iv)
        else:
            print("Unknown")

    # Tener en cuenta para los dos tipos de tarjeta añadir la descripción, el uid, y el atr (revisar si da alguna información relevante)
        

    except Exception as e:
        print(f"An error ocurred: {str(e)}")


if __name__ == "__main__":
    main()