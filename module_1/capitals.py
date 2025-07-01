def capitals(word):
    return [
        i for i, letter in enumerate(word) if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ]
