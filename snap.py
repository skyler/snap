import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import lib.menu
import lib.term
import lib.box
import lib.rsync
import lib.ssh
import subprocess

def main():
    menu = {
            "Snap to a node group": snap_group,
            "Snap to a node":snap_node,
            "Snap to testing node": snap_testing
           }

    lib.menu.navigate("Choose action",menu)()

    done_menu = {
                    "Return to main menu": "r",
                    "Exit":                "e"
                }
    next_action = lib.menu.navigate("Snap done, what do?",done_menu,clear_before=False)
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

def snap_testing():
    node = lib.box.getNode("testy")
    snap_project([node])

def snap_project(destinations):
    project = lib.menu.navigate("Choose project",lib.box.projects)
    branch  = project.choose_and_checkout_branch()
    manifest = project.get_manifest()

    lib.term.clear()
    lib.menu.project_check(project)

    for (command,payload) in manifest:
        print()
        command_ret = process_command(project,destinations,command,payload)

        if not command_ret and not lib.term.choice("Do you want to continue with the snap?",False):
            return

def process_command(project,destinations,command,payload):
    if command == "stage":
        return do_stage(project,payload,destinations)

    elif command == "local-script":
        return do_local_script(project,payload)

    elif command == "remote-script":
        return do_remote_script(project,payload,destinations)

    elif command == "choice":
        title,choices = payload
        newcommand,newpayload = lib.menu.navigate(title,choices,clear_before=False)
        print()
        return process_command(project,destinations,newcommand,newpayload)

    elif command == "pass":
        return True

    return True

def do_stage(project,stages,destinations):
    for node in destinations:
        for stage in stages:
            lib.menu.header("Snapping {0} to {1}".format(stage,node.name))
            try:
                lib.rsync.rsync(project,node,stage)
            except Exception as e:
                lib.term.big_error(str(e))
                return False
    return True

def do_local_script(project,script):
    lib.menu.header("Running {0} locally".format(script))
    try:
        project.snap_script(script)
    except Exception as e:
        lib.term.big_error(str(e))
        return False
    return True

def do_remote_script(project,script,destinations):
    for node in destinations:
        lib.menu.header("Running {0} script on {1}".format(script,node.name))
        try:
            lib.ssh.ssh_project(node,project,"chmod +x snap/{0} && snap/{0}".format(script))
        except Exception as e:
            lib.term.big_error(str(e))
            return False
    return True

#Run when everything is set up
main()
