## CODING CHALLENGE 3
# Part 2: push sys.argv to the limit

import sys
print("Alternative Names You Call Your Pets...")
def main(arg):
    print("Their Actual Name: " + str(arg))
main(sys.argv[1])

def main(arg):
    print("Something Dumb (because they can't speak English and how would they know): " + str(arg))
main(sys.argv[2])

def main(arg):
    print("Something Grossly Cute: " + str(arg))
main(sys.argv[3])