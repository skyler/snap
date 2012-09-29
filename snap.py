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
    project.pre_snap()
    lib.rsync.rsync(project,node)


#Run when everything is set up
main()
