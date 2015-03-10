import os
import errno
import subprocess

def mkdir_p(path):
    '''Recursively make all directories in a path'''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def dict_sorted(d):
    '''Returns dict sorted by key as a list of tuples'''
    return sorted(d.items(), key=lambda x: x[0])

def command_check_error(command,cwd=".",fail_on_stderr=True):
    '''Perform a command, piping out both stdout and stderr.

    An exception will be raised if command returns a nonzero exit code.
    An exception will also be raised if command writes anything to stdout.
    This behavior can be disabled by passing False as the argument to
    fail_on_stderr.
    '''
    proc = subprocess.Popen(command, cwd=cwd,
                            stdout=None, # print to terminal
                            stderr=subprocess.PIPE)
    dup  = subprocess.Popen(["tee","/dev/stderr"], stdin=proc.stderr,
                            stdout=subprocess.PIPE, # catch errors from first
                            stderr=None) # also print them to terminal
    errors = str(dup.stdout.read(),'utf8')
    proc.communicate()

    if proc.returncode != 0:
        raise Exception("{0} returned exit code {1}".format(command,proc.returncode))
    elif fail_on_stderr and errors:
        raise Exception("There was error output running {0}:\n{1}".format(command,errors))
