import sys
import lib.term

def navigate(title,menu):
    '''Given a menu title and a dict, has the user navigate the dict as if it was a menu.

    The user is displayed all the keys of the dicts as options, and they can select by
    either option number or by typing in the option name itself. If the selected value
    is valid it is returned, unless it is a dict in which case it is processed as another
    menu.
    '''
    #setup
    menu_numeric = []
    i = 0
    
    #Do the actual printing
    lib.term.clear()
    header(title)
    print()
    for (k,v) in menu.items():
        print("{0}) {1}".format(i,k))
        menu_numeric.append((k,v))
        i+=1
    lib.term.print_c("\nChoose an option (by number or name): ",lib.term.GREEN)
    
    #Read and strip the input
    choice = sys.stdin.readline().rstrip()
    
    try:
        try:
            #If choice is an integer return from the list
            choice = int(choice)
            (choice,choice_val) = menu_numeric[choice]
        except ValueError:
            #otherwise return from the dict
            choice_val = menu[choice]
    except:
        #If they chose something invalid we'll end up here. Tell them to try again
        print_c("Invalid menu choice, try again (hit enter)\n\n",lib.term.RED)
        sys.stdin.readline()
        return navigate(title,menu)

    #If the choice is a dict, do it all again!
    if isinstance(choice_val,dict):
        return navigate(choice,choice_val)
    #Otherwise return our val
    else:
        return choice_val

def header(title):
    eq = "="*(len(title)+4)
    lib.term.print_c("{0}\n= {1} =\n{0}\n".format(eq,title),lib.term.GREEN)
