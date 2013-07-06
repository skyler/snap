class node:

    def __init__(self,name,ip,ssh_port=22,groups=[]):
        self.name     = name
        self.ip       = ip
        self.ssh_port = ssh_port
        self.groups   = groups
