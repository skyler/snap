import os
import config
from lib.util import command_check_stderr

def ssh(node,command,cwd="/tmp"):
    '''ssh's into a node and runs command, cd-ing into cwd first'''

    ssh_command = "cd {0} && {1}".format(cwd,command)
    command = ["ssh","-t","-q","-p22","-i","snap_key","ccsnap@{0}".format(node["externalips"][0]),ssh_command]
    print(str.join(" ",command[:-1])+" '{0}'".format(ssh_command))

    command_check_stderr(command)

def ssh_project(node,project,command):
    '''Same as ssh, but cwds into a project's directory first'''
    project_path = project.location
    if config.testmode: project_path = config.testmode_prefix+project_path
    ssh(node,command,cwd=project_path)
