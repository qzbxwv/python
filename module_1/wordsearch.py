def word_search(query, seq):
    found = [word for word in query if seq.lower() in word.lower()]
    return found if found else []


print(word_search(input().strip(), input()))
