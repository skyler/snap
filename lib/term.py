import sys

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
PURPLE = "\033[35m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_c(text,colors):
    '''Prints a string with the given colors

    Example: print_c("hello world",RED+BOLD)
    '''
    sys.stdout.write(colors+text+RESET)

def clear():
    '''Clears terminal'''
    print(chr(27)+chr(91)+'H'+chr(27)+chr(91)+'J')
