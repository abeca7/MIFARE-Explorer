# Default Key Number
keyNumber = 0x00

# APDU Commands
GET_UID         = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Get UID command
GET_VERSION     = [0x90, 0x60, 0x00, 0x00, 0x00]  # Get Version command for DESFire
NEXT_FRAME      = [0x90, 0xAF, 0x00, 0x00, 0x00] # Next Frame for version, DESFire Get Version command // Similar to GetResponse
AUTHENTICATE    = [0x90, 0x0A, 0x00, 0x00, 0x01, keyNumber, 0x00]  # Authenticate command for DESFire
AUTH_CLAS       = lambda block_number, key_type: [0xFF, 0x88, 0x00, block_number, key_type, 0x00]  # Authenticate command for Classic
READ_BINARY     = lambda block_number: [0XFF, 0XB0, 0X00, block_number, 0X10] # Lambda function to create a command to read a binary block from the card.
WRITE_BINARY    = lambda block_number, data: [0xFF, 0xD6, 0x00, block_number, 0x10] + data # Lambda function to create a command to write a binary block to the card.
SELECT_FILE     = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00] # Select file command
LOADKEY         = [0xFF, 0x82, 0x00, keyNumber, 0x06] # Load key command




# Checkear que comandos se van a utilizar realmente
