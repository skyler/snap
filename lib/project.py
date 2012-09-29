import lib.util
import os
import subprocess

class project:

    def __init__(self,json):
        self.name   = json["name"]
        self.url    = json["url"]

    def clone(self):
        '''Clones project into cache, unless it's already there'''
        lib.util.mkdir_p(cache_path())
        if not os.path.isdir( os.path.join( project_cache_path(self.name), '.git' ) ):
            os.system("git clone {0} {1}".format(self.url, project_cache_path(self.name)))

    def fetch(self):
        '''Fetches all remote data'''
        self.clone()
        subprocess.call(["git","fetch","-v","--all"],
                        cwd=project_cache_path(self.name))

    def branches(self):
        '''Lists all current remote braches'''
        self.fetch()
        out = str(subprocess.check_output(["git","branch","-r"],
                                          cwd=project_cache_path(self.name)),'utf8')
        branches = []
        for branch in out.split("\n"):
            if not "HEAD" in branch:
                try: 
                    branches.append(branch.split("/")[1])
                except Exception: pass
        return branches

    def checkout(self,branch):
        self.fetch()
        cwd = project_cache_path(self.name)
        subprocess.call(["git","branch","-f",branch],cwd=cwd)
        subprocess.call(["git","checkout",branch],cwd=cwd)
        subprocess.call(["git","reset","--hard","origin/"+branch],cwd=cwd)
        

def cache_path():
    return os.path.join('.cache','repos')

def project_cache_path(proj):
    return os.path.join(cache_path(),proj)


