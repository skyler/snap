import lib.menu
import lib.term
import lib.box
import lib.rsync
import os
import subprocess

def main():
    project = lib.menu.navigate("Choose project",lib.box.projects)
    branch  = project.choose_and_checkout_branch()
    node = lib.box.getNode("testy")

    stages = project.get_stages()
    for stage in stages:
        if stage["pre"] != False:
            project.snap_script(stage["pre"])
        for line in stage["lines"]:
            lib.rsync.rsync(project,node,line)

    project.post_snap()


#Run when everything is set up
main()
