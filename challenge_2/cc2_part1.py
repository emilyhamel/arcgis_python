# CODING CHALLENGE 2
# Part 1: list values


# Make a new list that has all the elements less than 5 from this list in it and print out this new list.
# Write this in one line of Python (you do not need to append to a list just print the output).

value_list = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
new_list = [integer for integer in value_list if integer > 5]
print(new_list)
