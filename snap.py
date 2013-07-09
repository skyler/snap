import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import lib.menu
import lib.term
import lib.box
import lib.dsl
import subprocess

__ORIGINAL_PATH__ = list(sys.path)

def main():
    #Restore the original path, in case previous action messed it up
    sys.path = list(__ORIGINAL_PATH__)
    menu = {
            "Snap to a node group": snap_group,
            "Snap to a node":snap_node
           }

    lib.menu.navigate("Choose action",menu)()

    done_menu = {
                    "Return to main menu": "r",
                    "Exit":                "e"
                }
    next_action = lib.menu.navigate("Snap done, what do?",done_menu,clear_before=False)
    #TODO make this not suck
    if next_action == "r":
        main()
    else:
        pass

def snap_group():
    group = lib.menu.navigate("Choose group to snap to",lib.box.groups,depth=0)
    snap_project(group)

def snap_node():
    node = lib.menu.navigate("Choose node to snap to",lib.box.nodes,depth=0)
    snap_project([node])

def snap_project(destinations):
    project = lib.menu.navigate("Choose project",lib.box.projects)
    project.choose_and_checkout_branch()

    nosnap = project.get_nosnap()
    if not nosnap is None:
        print()
        lib.term.print_c(
            "Project has a nosnap file in its root.\nThe contents are:\n",
            lib.term.RED
        )
        print(nosnap)
        return

    lib.menu.project_check(project)

    snap_dir = project.get_snap_dir()
    pdsl = lib.dsl.dsl(project,destinations)
    if os.path.exists(os.path.join(snap_dir,"manifest.py")):
        sys.path.append(snap_dir)
        import manifest
        manifest.run(pdsl)
    else:
        lib.dsl.default_run(pdsl)

    if not pdsl.tagmsg is None:
        lib.menu.header("Tagging project")
        project.tag(pdsl.tagmsg)

#Run when everything is set up
main()
