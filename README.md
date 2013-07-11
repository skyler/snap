# Snap

A code push-deployment tool writtin in python.

## Philosophy

The goal of snap is to make it easy for a codebase to dictate its deployment procedures itself, and
not have that information exist somewhere else (in a chef repo, for instance). Snap reads deployment
procedures from a file inside the repo itself, meaning that the procedure can be easily changed and
tested without leaving the development environment, and can be different on a per-branch basis.

Snap is anti-parallel. This is based on the author's view that parallelism in the snap processes is
sometimes (in the author's experience: often) used to try to beat race-conditions. The problem is that
parallelism doesn't, and will never, solve the problem of race conditions during deployment. Only a
proper deployment procedure can do that. By doing everything single-threaded/serially, snap makes
race-conditions extremely obvious.

## Requirements

The following need to be installed for snap to work:
* Python 3
* git
* rsync
* ssh

## Setup

At this moment snap doesn't need a virtualenv environment to run; it works fine using just default
packages. The setup procedure is:

```bash
git clone https://github.com/cryptic-io/snap.git
cd snap
cp config.py.template config.py
#Edit config.py
```

To run snap simply:

```bash
python snap.py
```

### config.py

`config.py` is a python file which contains configuration information about snap (go figure). There's
two main kinds of items that `config.py` specifies. Keep in mind that `config.py` is a normal python
file, so all configuration can be generated from some other source and simple imported into snap.

#### Projects

All projects, or repositories, are specified in `config.py`. For each project it is required that you
specify:

* `name`: The name of the project, can't be the same as the name of any other project.
* `url`: The url of the git repository for the project.
* `location`: The location in the filesystem you want to snap to. This should be an absolute path.

You can also specify:

* `remote_user`: The user you want to own the snapped resources on the remote system. This user must be
                 able to write to the parent of the `location`. This parameter defaults to whatever
                 the name of the local user running snap is.
* `remote_user_key`: The location of the private ssh key to use when snapping. The private ssh key of
                     the local user running snap is used if this isn't specified.

#### Nodes

Nodes are other computers that snap can access and push resources to. For each node it is required
that you specify:

* `name`: An identifier for the node. The hostname will do fine.
* `ip`: The ip address or hostname of the node.

You can also specify:

* `ssh_port`: The ssh port to access the node through. Defaults to 22.
* `groups`: A list of strings, each string being the name of a group the node belongs to. When
            snapping you will be given the option of snapping to either an individual node or a group
            of node. This field is what snap uses to consolidate nodes into their respective groups.

### manifest.py

Each project that snap is set up should have a `snap` folder in its root, and in that folder there
should be a file called `manifest.py`. An example `manifest.py` looks like this:

```python
def run(self):
    self.local_script("test1")
    self.stage('.', includes=['foo'], excludes=['bar'])

    cdns = self.get_nodes_in_group("cdn")
    self.stage('.', includes=['foo'], excludes=['bar'], destinations=cdn)

    self.remote_script("test2", destinations=cdns)
```

The `def run(self):` section is required in every manifest. It's needed for snap to have something to
import. The rest of the statements, and more, will be explained next.

#### self.get_nodes(nodenames)

This function can be used to return the node objects with the given names. This can be used in
subsequent calls if your deployment procedure requires you to interact with nodes separate from the
main set you chose to snap to in the initial snap process.

#### self.get_nodes_in_group(groupname)

This function can be used to return the node objects within the given group name. This can be used in
subsequent calls if your deployment procedure requires you to interact with nodes separate from the
main set you chose to snap to in the initial snap process.

#### self.stage(directory, includes=[], excludes=[], destinations=None)

The bread and butter of snap, `stage` is used to actually put files in their remote locations (as
specified by the `location` directive in the project configuration).

`directory` is the directory within the project you want to snap. For instance, if you only want to
snap the directory `imgs` in your project, you would call: `self.stage('imgs/')`, and snap would
synchronize the local `<project root>/imgs` folder with the remote `<location>/imgs` folder.

`includes` and `excludes` are lists of strings which are passed through to rsync. They can be the
names of files, directories, or they can be globs (strings with `*`'s). Includes take precedence over
excludes, so if you wanted to only snap the file `README.md` in the root of your project without
touching anything else you would call `self.snap('.', includes=['README.md'], excludes=['*'])`.

`destinations` is by default `None`, which will cause `stage` to send the files only to the nodes you
chose in the menu leading up to the actual snap. If you want to have a part of your snap process
send files to a different set of nodes, you can pass a list of node objects (obtained through
`self.get_node` or `self.get_nodes_in_group`) here.

The function will return a boolean of whether or not the run was successful.

#### self.local_script(scriptname)

This will run a script in the local cache of the project. This script should be located alongside
`manifest.py` in the `snap/` folder in the repository, however the script will be run with the `cwd`
being the root of the repository (the parent of the `snap/` folder). The script will be run as is,
so as long as a shebang line is set the language used does not matter.

The function will return a boolean representing whether the run failed or not. Any output to stderr
by the script will constitute and error.

#### self.remote_script(scriptname, destinations=None)

This will run a script on all of the remote machines either in the set chosen in the menu or the ones
in `destinations` (see `self.stage` for more detail on `destinations`). The script should be located
alongside the `manifest.py` in the `snap/` directory in the root of the project, and will be run with
`cwd` being the root of the repository (the parent of the `snap/` folder). The script will be run as
is, so as long as a shebang line is set the language used does not matter.

The function will return a boolean representing whether the run failed or not. Any output to stderr
by the script will constitute and error.

#### self.header(string)

Prints out `string` in a nice little header that looks pretty. Has no actual utility other then for
maybe debugging.

#### self.choice(string,menu)

Offer the user doing the snapping a choice. `string` will be used as the title, menu is a dictionary,
where each key is the string which will be shown to the user in the menu selection, and each value is
what the function will return if that key was selected.

If the value is another map, `self.choice` will call itself on that map instead of returning. In this
way you can have nested menus.

#### self.tag(string)

Set the string you want to tag this snap with. If you set `string` to None then no tagging will take
place. This overwrites whatever is set in `config.py`.

(This statement is delayed, tagging will not take place until the snap is complete, and only one tag
can be done)

#### self.wentlive(src=config.wentlive_source, dest=config.wentlive_destination):

Use this to specify that you want to send a wentlive email, and optionally the email the wentlive
should appear to come from (`src`) and where it should go (`dest`, which can be either an email as a
string or a list of email strings). Overwrites whatever is set in `config.py`.

(This statement is delayed, sending of the wentlive will not take place until the snap is complete,
and only one wentlive can be sent out)

#### self.no_wentlive()

Use this to specify that no wentlive should be sent. Overwrites whatever is set in `config.py`

### Default manifest

If no `manifest.py` file is found in the `snap/` folder of the project, the default snap procedure
will be used:

```python
def default_run(self):
    self.stage('.')
```

# Supporters

The following companies/individuals supported the development of snap (and are awesome):

* [Coefficient, Inc](http://www.coefficientinc.com/)

