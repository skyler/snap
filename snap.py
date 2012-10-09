import lib.menu
import lib.term
import lib.box
import lib.rsync
import lib.ssh
import os
import subprocess

def main():
    menu = {
            "Snap to a node group": snap_group,
            "Snap to testing node": snap_testing
           }

    lib.menu.navigate("Choose action",menu)()

def snap_group():
    group = lib.menu.navigate("Choose group to snap to",lib.box.groups,depth=0)
    snap_project(group)

def snap_testing():
    node = lib.box.getNode("testy")
    snap_project({"testy":node})

def snap_project(destinations):
    project = lib.menu.navigate("Choose project",lib.box.projects)
    branch  = project.choose_and_checkout_branch()
    stages  = project.get_stages()

    for stage in stages:
        if stage["pre"] != False:
            print()
            lib.menu.header("(Stage {0}) pre-snap".format(stage["stage"]))
            project.snap_script(stage["pre"])
        for (node_name,node) in destinations.items():
            print()
            lib.menu.header("(Stage {0}) snapping to {1}".format(stage["stage"],node_name))
            for line in stage["lines"]:
                lib.rsync.rsync(project,node,line)

    if project.has_post_snap():
        for (node_name,node) in destinations.items():
            print()
            lib.menu.header("Running post snap script on {0}".format(node_name))
            lib.ssh.ssh_project(node,"chmod +x snap/post_snap && snap/post_snap",project)

#Run when everything is set up
main()
