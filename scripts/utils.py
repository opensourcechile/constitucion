def to_title_format(string):
    string = remove_special_chars(string)
    return string.replace('_', ' ').capitalize()

def remove_special_chars(string):
    string = str(string)
    special_chars = ['º','°',':','.']
    for char in special_chars:
        string = string.replace(char, '')
    return string
