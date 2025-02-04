def search_atr(atr_dict, atr_to_search):
    """
    Searches for an ATR in the dictionary and returns its card type and description.

    :param atr_dict: Dictionary containing ATRs.
    :param atr_to_search: The ATR to search for (spaces removed).
    :return: Dictionary with 'card_type' and 'description', or a default message if not found.
    """
    atr_to_search = atr_to_search.replace(" ", "").upper()
    return atr_dict.get(atr_to_search, {"card_type": "Unknown", "description": ["ATR not found"]})
