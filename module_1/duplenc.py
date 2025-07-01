from collections import Counter


def duplicate_encode(word):
    word_low = word.lower()
    counts = Counter(word_low)
    return "".join([")" if counts[char] > 1 else "(" for char in word_low])
