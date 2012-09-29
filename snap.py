import lib.menu
import lib.term
import lib.box
import os
import subprocess

def main():
    project = lib.menu.navigate("Choose project",lib.box.projects)
    branch  = project.choose_and_checkout_branch()
    node = lib.box.getNode("testy")

    command = "rsync -av --delete --exclude=.git -e'/usr/bin/ssh -i {0} -p22' {1} ccsnap@{2}:/opt/cc".format(
        os.path.join(os.getcwd(),"snap_key"),
        project.get_cache_path(),
        node["externalips"][0]
        )
    print(command)
    os.system(command)

#Run when everything is set up
main()
