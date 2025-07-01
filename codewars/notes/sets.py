# set is uniq list
lst = [1, 2, 3, 4, 5, 1]
print(lst)
unq_lst = list(set(lst))
print(unq_lst)

# it very faster than list to iterate

# to create set
my_set = {1, 2, 3}
print(my_set)
# or
my_set_new = set()
print(my_set_new)

# to add
my_set.add(4)
print(my_set)

# to remove
my_set.remove(4)
print(my_set)
# or discard without error
my_set.discard(4)  # nothing to discard but don`t gives an error
print(my_set)

# operations
# union two sets
set1 = {1, 2, 3}
set2 = {4, 5, 6}
set1 = set1.union(set2)  # or |
print(set1)
# intersection
print(
    set1.intersection(set2)
)  # the elements which are contained in both sets is returned.

# different
diff_set_1 = {1, 2, 3}
diff_set_2 = {4, 5, 6}

print(diff_set_1.difference(diff_set_2))

#  frozenset is like tuple for lst
my_dict = {frozenset([1, 2]): "value"}  # key:value
print(my_dict.keys())
