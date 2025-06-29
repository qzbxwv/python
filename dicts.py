person = {
    # key:value
    "Name": "qzbx",
    "Age": 16,
    "Job": "AI full-stack dev",
    "Intelligence": "Infinity",
}

name = person["Name"]
age = person["Age"]
job = person["Job"]
intelligence = person["Intelligence"]

print(f"Name is {name}")
print(f"His age is {age}")
print(f"Future job is {job}")
print(f"His intelligence is {intelligence}")

# We can modify our person by
person["Age"] = 17

print(f"Updated person is {person}")

# We can append our person by
person["Sex"] = "Male"
person["Hobbies"] = ["Programming", "Architect", "GYM"]
print("New hobbies and sex: ", person)

# We can delete by
del person["Sex"]

print("Person without sex ;): ", person)

# We can convert dict to list

person_copy = person

person_lst = list(person_copy.items())  # items method
print(person_lst)

# Keys method
print(person.keys())

# but we can do it like cycle

for key in person:
    print(f"Key: {key}")

# Values method does the same but with values

print(person.values())

# And we can iterate it but with value method
for value in person.values():
    print(f"Value: {value}")

# lists into dict by dict(zip())
cities = ["Gomel", "Minsk", "Brest", "Mogilev", "Vitebsk", "Grodno"]
country = ["Belarus", "Belarus", "Belarus", "Belarus", "Belarus", "Belarus"]

# dict(zip(key, value))
cities_and_county = dict(zip(cities, country))
print(cities_and_county)

# every key is unique, the last value wins
uniq_example = {"value_1": 1, "value_2": 2, "value_1": 3}
print(uniq_example)

# dict can contain other dict as value
dict_1_cont = {"v1": 1, "v2": 2, "v3": 3}
dict_2_cont = {"v4": 4, "v5": 5, "v6": 6}

dict_that_cont_1_and_2 = {"first": dict_1_cont, "second": dict_2_cont}
print(dict_that_cont_1_and_2)
print(dict_that_cont_1_and_2["first"]["v2"])  # eq to first['v2']

# pop method key:value pair will be removed, and pop() will return value of key

pop_dict1 = dict_1_cont.pop("v1")
print(pop_dict1)
print(dict_1_cont)

# get() needs to access the value via key
print(person.get("Age"))
# its like
print(person["Age"])

# Copy dict via copy()
person2 = person.copy()
print(person2)
# To remove all data from dict and make it clear we use clear()

person2.clear()
print("This is person 2 but cleared ", person2)

# Update dict is like merge dict
dict_up_1 = {"v1": 1, "v2": 2, "v3": 3}
dict_up_2 = {"v3": 3, "v4": 4, "v5": 5}
dict_up_1.update(dict_up_2)
print(dict_up_1)
