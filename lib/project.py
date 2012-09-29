import lib.util
import lib.menu
import os
import subprocess

git_env = os.environ.copy()
git_env["GIT_SSH"] = os.path.join(os.getcwd(),"ssh_wrapper.sh")

class project:

    def __init__(self,json):
        self.name    = json["name"]
        self.url     = json["url"]
        self.fetched = False

    def clone(self):
        '''Clones project into cache, unless it's already there'''
        lib.util.mkdir_p(cache_path())
        if not os.path.isdir( os.path.join( project_cache_path(self.name), '.git' ) ):
            subprocess.call(["git","clone",self.url],cwd=cache_path(),env=git_env)

    def fetch(self):
        '''Fetches all remote data'''
        self.clone()
        if not self.fetched:
            self.fetched = True
            subprocess.call(["git","fetch","-v","--all"],
                            cwd=project_cache_path(self.name),
                            env=git_env)

    def branches(self):
        '''Lists all current remote braches'''
        self.fetch()
        out = str(subprocess.check_output(["git","branch","-r"],
                                          cwd=project_cache_path(self.name),
                                          env=git_env),'utf8')
        branches = []
        for branch in out.split("\n"):
            if not "HEAD" in branch:
                try: 
                    branches.append(branch.split("/")[1])
                except Exception: pass
        return branches

    def checkout(self,branch):
        '''Checks out the given branch in the local cache repo, does a hard reset'''
        self.fetch()
        cwd = project_cache_path(self.name)
        with open(os.devnull) as null:
            subprocess.call(["git","branch","-f",branch],stdout=null,stderr=null,cwd=cwd)
            subprocess.call(["git","checkout",branch],stdout=null,stderr=null,cwd=cwd)
            subprocess.call(["git","reset","--hard","origin/"+branch],cwd=cwd)
        

def cache_path():
    '''Return relative path to repo cache'''
    return os.path.join('.cache','repos')

def project_cache_path(proj):
    '''Return relative path to project's repo cache'''
    return os.path.join(cache_path(),proj)

def choose_and_checkout_branch(project):
    branches = {}
    for b in project.branches():
        branches[b] = b
    branch = lib.menu.navigate("Choose a branch from {0}".format(project.name),branches)
    project.checkout(branch)
    return branch
