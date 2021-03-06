## CODING CHALLENGE 3
# Part 1: directory tree

import os

# using os.mkdir to create the tree is the order outlined in the assignment description
# the "challenge_3" folder contains the entire directory tree
dir_tree = r"C:\challenge_3"
os.mkdir(dir_tree)
os.mkdir(os.path.join(dir_tree, "draft_code"))
os.mkdir(os.path.join(dir_tree, "draft_code\pending"))
os.mkdir(os.path.join(dir_tree, "draft_code\complete"))
os.mkdir(os.path.join(dir_tree, "includes"))
os.mkdir(r"C:\challenge_3\layouts")
os.mkdir(r"C:\challenge_3\layouts\default")
os.mkdir(r"C:\challenge_3\layouts\post")
os.mkdir(r"C:\challenge_3\layouts\post\posted")
os.mkdir(r"C:\challenge_3\site")

# deleting the directory tree
import shutil

shutil.rmtree(dir_tree)
