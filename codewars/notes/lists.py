lst = [1, 2, 3]

# append element to lst
lst.append(4)
# lst = lst.append(4) : None

print(lst)

# delete element from lst
lst.pop(1)  # delete 1 element from lst

print(lst)

lst.pop()  # without an argument returns -1

print(lst)

# extend lst
# we use extend
lst.extend([5, 6])

print(lst)

# alternative is + or += but only with words

word_lst = ["I", "like", "python"]
word_lst += "!"

print(word_lst)

# removing
lst.remove(1)  # removes first occurrence of 1 in lst

# find position of an element in lst
print(lst.index(3))
# index(elem, from, to)
print(lst.index(5, 1, 3))

# insert elem in index
# insert(index, elem)

lst.insert(3, 7)

print(lst)

# we can simulate append method by len

lst.insert(len(lst), 10)

print(lst)
