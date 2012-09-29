import config
import os
import subprocess

def rsync(project,node,files='.'):

    excludes = ""
    for e in get_default_excludes()+project.get_excludes():
        excludes += "--exclude={0} ".format(e)

    includes = ""
    for i in project.get_includes():
        includes += "--include={0} ".format(i)

    command = "rsync -av --delete {3}{4}-e'/usr/bin/ssh -i {0} -p22' --rsync-path='mkdir -p {5} && rsync' {1} ccsnap@{2}:{5}".format(
        os.path.join(os.getcwd(),"snap_key"),
        os.path.join(project.get_cache_path(),files),
        node["externalips"][0],
        excludes,
        includes,
        config.snap_prefix+"/opt/cc/"+project.name
    )

    print(command)
    os.system(command)
    

def get_default_excludes():
    excludes = []
    with open("res/default_excludes") as f:
        for line in f:
            excludes.append(line.rstrip())
    return excludes
