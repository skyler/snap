import lib.menu
import lib.term
import lib.box

def main():
    project = lib.menu.navigate("Choose project",lib.box.projects)
    branch  = lib.project.choose_and_checkout_branch(project)

#Run when everything is set up
main()
