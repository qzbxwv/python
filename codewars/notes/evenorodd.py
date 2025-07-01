# first kata 8 kyu
# my solution


def even_or_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"


# best practices
def even_or_odd_best(number):
    return "Odd" if number % 2 else "Even"
    # number % 0 = False, other True
