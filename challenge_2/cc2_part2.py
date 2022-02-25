# CODING CHALLENGE 2
# Part 2: list overlap


# Determine which items are present in both lists.
list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']
for x in list_a:
    for y in list_b:
        if x == y:
            print(x)

# Determine which items do not overlap in the lists.
list_diff = [x for x in list_a if x not in list_b]
list_diff.extend(y for y in list_b if y not in list_a)
print(list_diff)


# AD - Nice nice nice!
