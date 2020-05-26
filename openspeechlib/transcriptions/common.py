
STOP_SYMBOLS = r'[:; ,\n\r()¿¡!]'


def clean_accents(word):
    output = []
    for letter in word:
        if letter == "á":
            modified_letter = "a"
        elif letter == "é":
            modified_letter = "e"
        elif letter == "í":
            modified_letter = "i"
        elif letter == "ó":
            modified_letter = "o"
        elif letter == "ú":
            modified_letter = "u"
        elif letter == "ñ":
            modified_letter = "N"
        else:
            modified_letter = letter
        output.append(modified_letter)
    return ''.join(output)


def filter_special_characters(word):
    output = []
    for letter in word:
        if letter == "-":
            modified_letter = ""
        elif letter == "\n":
            modified_letter = ""
        elif letter == ".":
            modified_letter = ""
        elif letter == "?":
            modified_letter = ""
        else:
            modified_letter = letter
        output.append(modified_letter)
    return ''.join(output)


def allow_characters(word):
    alphabet = "abcdefghijklmnNopqrstuvwxyz "
    output = []
    for letter in word:
        if letter in alphabet:
            output.append(letter)
    return ''.join(output)


def extract_phones_from_word(word):
    return ' '.join(apply_filters(word))


def apply_filters(word):
    return allow_characters(filter_special_characters(clean_accents(word)))


def remove_jump_characters(word):
    return word.replace("\n", "").replace("\r", "")
