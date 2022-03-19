import os

import svg_tools

try:
    columns, rows = os.get_terminal_size(0)
except OSError:
    columns, rows = os.get_terminal_size(1)


def print_centered(text):
    print(text.center(columns)[:-1])


print_centered("~~~ SVG to GD ~~~")
print_centered("Made by jaan and camila314")
print()
print_centered("It's recommended to backup your save files")
print_centered("if something goes wrong")
print()

running = True
while running:
    try:
        file_name = input("Specify file name(\"exit\" to close): ")
        if file_name == "exit":
            break
        scale = 1 / float(input("Specify scale(>1 => bigger): "))
        density = float(input("Specify density, distance between blocks(>1 => less): "))
        block_size = float(input("Specify block size: "))
        error_c = input("Error correction(y/n): ").lower() == "y"
        print()
        print("Converting...")
        svg_tools.generate(file_name, scale, density, block_size, error_c)
    except ValueError:
        print("Please enter a valid value.")

    print()
    print()
