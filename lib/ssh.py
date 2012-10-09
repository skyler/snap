import os
import config

def ssh(node,command,cwd="/tmp"):
    '''ssh's into a node and runs command, cd-ing into cwd first'''
    command = "ssh -p22 -i {0} ccsnap@{1} 'cd {2} && {3}'".format(
                os.path.join(os.getcwd(),"snap_key"),
                node["externalips"][0],
                cwd,
                command
              )
    print(command)
    os.system(command)

def ssh_project(node,command,project):
    '''Same as ssh, but cwds into a project's directory first'''
    ssh(node,command,cwd=
        os.path.join(config.snap_prefix,"opt/cc",project.name))
