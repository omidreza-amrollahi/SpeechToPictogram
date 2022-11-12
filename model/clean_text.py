def clean_text(text):
    """
    we get rid of the commas and dots, maybe in the future there more things to get rid of in a sentence like !, ? ...

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """
    text = text.lower()
    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = text.replace("?", " ")
    text = text.replace("-", " ")
    text = text.split()
    new_string = []
    for temp in text:
        if temp:
            new_string.append(temp)
    concatString = ' '.join(new_string)
    return new_string, concatString
