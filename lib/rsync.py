import config
import os
import subprocess
from lib.util import command_check_stderr

def rsync(project,node,files='.'):

    excludes = []
    for e in get_default_excludes()+project.get_excludes():
        excludes.append("--exclude={0}".format(e))

    includes = []
    for i in project.get_includes():
        includes.append("--include={0}".format(i))

    local_project_files  = os.path.join(project.get_cache_dir(),files)
    remote_project_path  = project.location
    if config.testmode: remote_project_path = config.testmode_prefix+remote_project_path

    key_stmt = ""
    if project.key:
        key_stmt = "-i {0}".format(os.path.join(os.getcwd(),project.key))

    command  = ["rsync", "-av", "--delete"]
    command += excludes
    command += includes
    command += ["-e",'/usr/bin/ssh {0} -p22'.format(key_stmt)]
    command += ["--rsync-path=mkdir -p {0} && rsync".format(remote_project_path)]
    command += [local_project_files]
    command += ["{0}@{1}:{2}".format(project.user,node["externalips"][0],remote_project_path)]

    print(command)

    command_check_stderr(command)


def get_default_excludes():
    excludes = []
    with open("res/default_excludes") as f:
        for line in f:
            excludes.append(line.rstrip())
    return excludes
