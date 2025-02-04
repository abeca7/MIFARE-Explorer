from Crypto.Cipher import DES

def parse_get_version(response):
    """
    Parse the response from the GetVersion command to extract detailed information.

    :param response: List of strings, where each string represents a frame from the GetVersion response.
    :return: Dictionary with parsed information.
    """
    # Initialize dictionaries to store the parsed information
    version_info = {}

    # Frame 1: Hardware version
    frame_1 = response[0].split()

    hard_info = {}
    if frame_1[0] == '04':
        hard_info['vendor'] = 'NXP'
    else:
        hard_info['vendor'] = 'Unknown'
    hard_info['type'] = f"{int(frame_1[1], 16)}.{int(frame_1[2], 16)}"
    hard_info['version'] = f"{int(frame_1[3], 16)}.{int(frame_1[4], 16)}"

    storage_code = int(frame_1[5], 16)
    n = storage_code >> 1  # Get the 7-MSbits
    if storage_code & 1 == 0:  # Check if the LSbit is '0'
        hard_info['storage_size'] = 2 ** n
    else:
        hard_info['storage_size'] = 2 ** n  # Adjust this if there's a different rule for LSbit '1'

    if frame_1[6] == '05':
        hard_info['protocol'] = 'ISO 14443-2 and -3'
    else:
        hard_info['protocol'] = 'Unknown'
    version_info['hardware_info'] = hard_info

    # Frame 2: Software version
    frame_2 = response[1].split()
    soft_info = {}
    if frame_1[0] == '04':
        soft_info['vendor'] = 'NXP'
    else:    
        soft_info['vendor'] = 'Unknown'    
    soft_info['type'] = f"{int(frame_2[1], 16)}.{int(frame_2[2], 16)}"
    soft_info['version'] = f"{int(frame_2[3], 16)}.{int(frame_2[4], 16)}"

    storage_code = int(frame_2[5], 16)
    n = storage_code >> 1  # Get the 7-MSbits
    if storage_code & 1 == 0:  # Check if the LSbit is '0'
        soft_info['storage_size'] = 2 ** n
    else:
        soft_info['storage_size'] = 2 ** n  # Adjust this if there's a different rule for LSbit '1'
    
    if frame_1[6] == '05':
        soft_info['protocol'] = 'ISO 14443-2 and -3'
    else:
        soft_info['protocol'] = 'Unknown'
    version_info['software_info'] = soft_info

    # Frame 3: Additional information
    frame_3 = response[2].split()
    #version_info['uid'] = '%02X%02X%02X%02X%02X%02X%02X' %(frame_3[0], frame_3[1], frame_3[2], frame_3[3], frame_3[4], frame_3[5], frame_3[6])


    # Combine all parsed information
    # REVISAR SI SE EL RETURN SE PUEDE MODIFICAR PARA ENVIAR SOLO LO NECESARIO
    return version_info

def encrypt(data, key, iv):
    """
    Encrypts data using DES in CBC mode.
    
    Args:
        data (string): Data to encrypt (8 bytes).
        key (bytes): 8-byte key for DES.
    
    Returns:
        bytes: Encrypted data.
    """
    # Convert the data from hex to bytes
    if type(data) == str:
        data_b = bytes.fromhex(data)
    else:
        data_b = data

    # Validate inputs
    if len(key) != 8:
        raise ValueError("The key must be exactly 8 bytes for DES.")
    if len(iv) != 8:
        raise ValueError("The IV must be exactly 8 bytes.")
    if len(data_b) % 8 != 0:
        raise ValueError("The plaintext must be a multiple of 8 bytes.")
    
    # Create the DES object in CBC mode
    des = DES.new(key, DES.MODE_CBC, iv)

    # The new IV is the last block of the ciphertext
    updated_iv = data_b[-8:]

    # Encrypt the data
    encrypted_data = des.encrypt(data_b)
    
    return list(encrypted_data), updated_iv

def decrypt(data, key, iv):
    """
    Decrypts data using DES in CBC mode.
    
    Args:
        data (string): Encrypted data.
        key (bytes): 8-byte key for DES.
    
    Returns:
        bytes: Decrypted data.
    """
    # Convert the data from hex to bytes
    if type(data) == str:
        data_b = bytes.fromhex(data)
    else:
        data_b = data

    if len(key) != 8:
        raise ValueError("The key must be exactly 8 bytes for DES.")
    
    # Create the DES object in ECB mode
    des = DES.new(key, DES.MODE_CBC, iv)

    # The new IV is the last block of the ciphertext
    updated_iv = data_b[-8:]
    
    # Decrypt the data
    decrypted_data = des.decrypt(data_b)
    return list(decrypted_data), updated_iv
