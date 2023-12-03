# Day 3, 1

# You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

# It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

# "Aaah!"

# You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

# The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

# The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

# Here is an example engine schematic:
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..

# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

import argparse

def get_lookup_position(file):
    with open(file) as f:
        lines = [line.rstrip() for line in f]

        max_rows = len(lines) # Max numbers of rows, to prevent crossing the lower bound
        max_len = len(lines[0]) # Max number of symbols in a line, to prevent crossing line
        number_res = [] # An array to save extracted number, and tuple with
        symbols = [] # An array where False indicate a non symbol, and True a symbol in the input array

        for row_n, line in enumerate(lines):
            number = '' # Creating string to save the number
            line_symbols = [] # Logical array to decode symbols
            for ind, it in enumerate(line):
                if it.isnumeric() and ind < max_len - 1:
                    number += it
                    line_symbols.append(False)
                elif it.isnumeric() and ind == max_len - 1:
                    line_symbols.append(False)
                    number += it
                    # Save the number if the line ends
                    x_range = (max(ind-len(number), 0), ind) # Case where iter reaches when end of the line
                    y_range = get_rows(row_n, max_rows)
                    number_res.append([number, (x_range, y_range)])
                else:
                    if number != '': # Case where the first non-number appears
                        x_range = (max(ind-len(number)-1, 0), ind) # Prevents negative indexing
                        y_range = get_rows(row_n, max_rows)
                        number_res.append([number, (x_range, y_range)])
                    number = ''
                    if it == '.':
                        line_symbols.append(False)
                    else:
                        line_symbols.append(True)
            symbols.append(line_symbols)
    return symbols, number_res, max_len


def get_rows(row_n, max_rows):
    """
    Define row lookup range
    :param row_n: current row where the number is located
    :param max_rows: max number of rows in the input
    :return:
    """
    y_range = []
    if row_n > 0:  # Check if there is a row above
        y_range.append(row_n - 1)

    y_range.append(row_n) # Add the current row

    if row_n + 1 <= max_rows - 1:  # Check if there is a below above, # max_rows - 1 cause python uses 0 based indexing
        y_range.append(row_n + 1)
    return y_range

def get_true_numbers(symb, positions, max_len):
    """
    Iterate over numbers and lookup ranges and look into corresponding array symb encoding if there is a sybmol
    :param symb: array encoding where are the symbols
    :param positions: array encoding number and coordinates
    :param max_len: max len of the line
    :return:
    """
    final = []
    for (number, coordinate) in positions:
        for row in coordinate[1]:
            if coordinate[0][1] == max_len:
                logical_array = symb[row][coordinate[0][0]:coordinate[0][1]]
            else:
                logical_array = symb[row][coordinate[0][0]:coordinate[0][1] +1]
            if any(logical_array):
                final.append(int(number))
                break
    return sum(final)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-file', '--file_name', default='/Users/kam/Desktop/3_1.txt',
                    help='File path')
    symbols, numberic_res, max_poss_len = get_lookup_position('/Users/kam/Desktop/3_1.txt')
    print(get_true_numbers(symbols, numberic_res, max_poss_len))
