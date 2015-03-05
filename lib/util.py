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
    
    #### FIXME
    By default, if anything comes out on stderr it will throw an exception.
    If `check_exit_code` is `True`, the command's exit code, if nonzero, will
    throw an exception. In this configuration, output to stderr, whatever it is,
    will be ignored as an error condition. Its output will still be raised
    as the exception body if the command's exit code was nonzero, however.
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
