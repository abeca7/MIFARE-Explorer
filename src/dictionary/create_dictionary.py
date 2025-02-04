def create_atr_dictionary(file_path="utils/atr_list.txt"):
    """
    Reads a text file with ATRs and creates a dictionary.
    Each ATR is a key, and its value is a dictionary with 'card_type' and 'description'.

    :param file_path: Path to the text file containing ATRs.
    :return: Dictionary with ATRs as keys and their details as values.
    """
    atr_dict = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            atr = None  # Temporary variable to hold the current ATR
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    # Skip empty lines or comments
                    continue

                if line.startswith("3B") or line.startswith("3F"):
                    # If the line starts with "3B" or "3F", it is an ATR (remove spaces)
                    atr = line.replace(" ", "").upper()
                    atr_dict[atr] = {"card_type": None, "description": []}
                elif atr and line:
                    # If there is a description or card_type associated with the current ATR
                    if line.upper() in ["CLASSIC", "DESFIRE"]:
                        # Assign the card type
                        atr_dict[atr]["card_type"] = line.upper()
                    else:
                        # Add the rest as description
                        atr_dict[atr]["description"].append(line.strip())
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"Error processing the file {file_path}: {e}")

    return atr_dict
