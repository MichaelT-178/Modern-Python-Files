# Updated version of NameStats.py. Written on 4/13/2023. Original was ~136 lines, this is ~35 lines.
og_name = input("Please enter your full name: ").strip()

while len(og_name.split(" ")) != 3:
    print('Please enter your first, middle, and last name.\n')
    og_name = input("Please enter your full name: ").strip()

highest_count = 0
name = og_name.upper()

for char in name:
    if name.count(char) > highest_count:
        highest_count = name.count(char)

print(f"\nYour name is {og_name}.")
print("These are the stats of your name.")
print("\nThese are the amounts of each letter in your name")

used = []

for i in range(highest_count + 1):
    for char in name:
        if name.count(char) == i and char != " " and char not in used:
            used.append(char)
            s = "'s" #cant use "\' or "" or ''' in string literal
            print(f"•There is {i} {char}{s if i != 1 else ''} in your name")
    print()

names = og_name.upper().split(' ')
print("Other Statistics")
print(f'•There is a total of {len(og_name.replace(" ", "")) } letters in your name.')
print(f"•There are {len(used)} different letters in your name.")
print(f"•Your name makes up approximately {((len(used)/26) * 100):.2f}% of the alphabet!")
print(f"•Your initials are \'{names[0][0]}{names[1][0]}{names[2][0]}\'.")
print(f"•You have a very special name {og_name.split(' ')[0]}! Congragulations!")