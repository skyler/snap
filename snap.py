import lib.menu
import lib.term
import lib.box

def main():
    print(lib.box.getProject('ccetc').checkout("master"))

#Run when everything is set up
main()
