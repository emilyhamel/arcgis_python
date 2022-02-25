# CODING CHALLENGE 2
# Part 3: given a singe phrase, count the occurrence of each word


# Count the occurrence of each word, and print the word plus the count

string = 'hi dee hi how are you mr dee'
list_string = string.split()
unique_words = set(list_string)
for words in unique_words:
    print(words, list_string.count(words))

# AD: Very nice solution to this challenge.