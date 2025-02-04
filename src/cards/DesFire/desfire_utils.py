from utils.des_operations import parse_get_version

def get_parsed_info(version_info):
    """
    Parse the response from the GetVersion command to extract detailed information.
    """
    version_parsed = parse_get_version(version_info)
    # Initilization of the variables vendor and double check to ensure that have the same value
    hard_vendor = version_parsed['hardware_info']['vendor']
    soft_vendor = version_parsed['software_info']['vendor']

    if hard_vendor  == soft_vendor:
        vendor = hard_vendor

    # Initialization of the variables type and double check to ensure that have the same value
    hard_type = version_parsed['hardware_info']['type']
    soft_type = version_parsed['software_info']['type']

    if hard_type == soft_type:
        major_version = hard_type.split('.')[0]
        if major_version == '1':
            type = f"{hard_type} - (MIFARE DESFire)"

    # Initialization of the variables version and double check to ensure that have the same value
    hard_storage_size = version_parsed['hardware_info']['storage_size']
    soft_storage_size = version_parsed['software_info']['storage_size']

    if hard_storage_size == soft_storage_size:
        storage_size = f"{hard_storage_size} bytes"

    # Initialization of the variables protocol and double check to ensure that have the same value
    hard_protocol = version_parsed['hardware_info']['protocol']
    soft_protocol = version_parsed['software_info']['protocol']

    if hard_protocol == soft_protocol:
        protocol = hard_protocol

    # Initialization of the variables version
    hard_version = version_parsed['hardware_info']['version']
    soft_version = version_parsed['software_info']['version']   

    # Check the software version to determine the DESFire card version
    major_version = soft_version.split('.')[0]
    if major_version == '1':
        card_version = 'EV1'
    elif major_version == '2':
        card_version = 'EV2'
    elif major_version == '3':
        card_version = 'EV3'
    else:
        card_version = 'Unknown'

    return vendor, type, storage_size, protocol, hard_version, soft_version, card_version