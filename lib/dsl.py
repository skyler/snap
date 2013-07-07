import config
import lib.rsync
import lib.menu
import lib.ssh

def default_run(self):
    self.stage('.')

class dsl:

    def __init__(self,project,destinations):
        self.project = project
        self.destinations = destinations

    def stage(self,stage,includes=None,excludes=None):
        if includes is None: includes = []
        if excludes is None: excludes = []
        for e in config.default_excludes:
            excludes.append(e)

        for node in self.destinations:
            lib.menu.header("Snapping {0} to {1}".format(stage,node.name))
            try:
                lib.rsync.rsync(self.project,node,stage,includes,excludes)
            except Exception as e:
                lib.term.big_error(str(e))
                return False
        return True

    def local_script(self,script):
        lib.menu.header("Running {0} locally".format(script))
        try:
            self.project.snap_script(script)
        except Exception as e:
            lib.term.big_error(str(e))
            return False
        return True

    #TODO make sure this is already sync'd
    def remote_script(self,script):
        for node in self.destinations:
            lib.menu.header("Running {0} script on {1}".format(script,node.name))
            try:
                lib.ssh.ssh_project(node,self.project,"chmod +x snap/{0} && snap/{0}".format(script))
            except Exception as e:
                lib.term.big_error(str(e))
                return False
        return True

    def header(self,title):
        return lib.menu.header(title,lib.term.BLUE)

    def choice(self,title,menu):
        return lib.menu.navigate(title,menu,clear_before=False)
