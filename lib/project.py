import lib.util
import lib.menu
import lib.term
import os
import subprocess
import re

git_env = os.environ.copy()
git_env["GIT_SSH"] = os.path.join(os.getcwd(),"ssh_wrapper.sh")

def cache_path():
    '''Return relative path to repo cache'''
    return os.path.join('.cache','repos')


class project:

    def __init__(self,json):
        self.name    = json["name"]
        self.url     = json["url"]
        self.fetched = False

    def clone(self):
        '''Clones project into cache, unless it's already there'''
        lib.util.mkdir_p(cache_path())
        if not os.path.isdir( os.path.join( self.get_cache_dir(), '.git' ) ):
            lib.term.print_c("Cloning...\n",lib.term.BLUE)
            subprocess.call(["git","clone",self.url],cwd=cache_path(),env=git_env)

    def fetch(self):
        '''Fetches all remote data'''
        self.clone()
        if not self.fetched:
            lib.term.print_c("Fetching....\n",lib.term.BLUE)
            self.fetched = True
            subprocess.call(["git","fetch","-v","--all"],
                            cwd=self.get_cache_dir(),
                            env=git_env)

    def branches(self):
        '''Lists all current remote braches'''
        self.fetch()
        subprocess.call(["git","remote","prune","origin"],cwd=self.get_cache_dir())
        out = str(subprocess.check_output(["git","branch","-r"],
                                          cwd=self.get_cache_dir(),
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
        cwd = self.get_cache_dir()
        lib.term.print_c("Checking out....\n",lib.term.BLUE)
        with open(os.devnull) as null:
            subprocess.call(["git","branch","-f",branch],stdout=null,stderr=null,cwd=cwd)
            subprocess.call(["git","checkout",branch],stdout=null,stderr=null,cwd=cwd)
            subprocess.call(["git","reset","--hard","origin/"+branch],cwd=cwd)
            subprocess.call(["git","clean","-f","-d"],cwd=cwd)

    def get_cache_dir(self):
        '''Return relative path to project's repo cache'''
        return os.path.join(cache_path(),self.name)

    def get_snap_dir(self):
        '''Returns full path to project's snap directory'''
        return os.path.join(self.get_cache_dir(),"snap")
        
    def choose_and_checkout_branch(self):
        '''Gives user list of branches to choose from, and checks out the chosen one'''
        branches = {}
        for b in self.branches():
            branches[b] = b
        branch = lib.menu.navigate("Choose a branch from {0}".format(self.name),branches)
        self.checkout(branch)
        return branch

    def get_snapfile_lines(self,fn):
        '''Returns lines from a file in the project's snap directory as a list,
        or empty list on error'''
        lines = []
        try:
            with open(os.path.join(self.get_snap_dir(),fn)) as f:
                for l in f:
                    lines.append(l.rstrip())
            return lines
        except Exception:
            return []

    def get_excludes(self):
        '''Returns project's excludes'''
        return self.get_snapfile_lines("excludes")

    def get_includes(self):
        '''Returns project's includes'''
        return self.get_snapfile_lines("includes")

    def get_manifest(self):
        '''Returns the lines of the manifest as a list of tuples. Possible tuples:

        ("stage",["filedir1","filedir2","...")
        ("local-script","script_name")
        ("remote-script","script_name")

        If there is no manifest file, pretends it had only the line "stage ."
        '''
        lines = self.get_snapfile_lines("manifest")
        manifest = []
        for line in lines:
            sline = re.findall('[^ ]+',line)
            command = sline[0]
            if command == "stage":
                stages = list(map(lambda x: x.strip(), sline[1:]))
                manifest.append(( "stage",stages))
            elif command == "local-script":
                ls = sline[1].strip()
                manifest.append(("local-script",ls))
            elif command == "remote-script":
                rs = sline[1].strip()
                manifest.append(("remote-script",rs)) 

        if manifest == []:
            manifest = [("stage",["."])]
        return manifest

    def snap_script(self,script):
        '''Runs a script in the snap directory'''
        cache_path = self.get_cache_dir()
        snap_path  = self.get_snap_dir()
        fn_abs = os.path.join( snap_path, script )
        fn_rel = os.path.join( "snap",    script )
        if os.path.isfile(fn_abs):
            os.system("chmod +x {0}".format(fn_abs))
            subprocess.call([fn_rel],cwd=cache_path)


