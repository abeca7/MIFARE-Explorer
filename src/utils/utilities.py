from smartcard.util import toHexString

# You can also put any common utilities or helper functions here.
def handle_apdu_response(sw1, sw2, response=None):
    if (sw1 == 0x90 and sw2 == 0x00 or sw1 == 0x91 and sw2 == 0xAF):
        return toHexString(response) if response else "Success"
    else:
        raise Exception(f"Failed, SW1: {hex(sw1)}, SW2: {hex(sw2)}")