from os import system, name

"""
Function that clears the terminal of all text rendered
"""
def clear():
    if name == 'nt':
        system('cls') # Windows Command
    else:
        system('clear') # Linux/Mac OS Command