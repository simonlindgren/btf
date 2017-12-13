import os

if input("This will delete ALL database files in this directory. Continue? (y/n)") != "y":
    exit()

files = os.listdir()

for item in files:
    if item.endswith(".db"):
        os.remove(item)

print("Removed!")
