import json
import sys
import os
import pprint
sys.path.append(
    os.path.join(
        os.environ['CCETC_ROOT']
    )
)
import ccetc_py.info
from lib.project import project

#Init projects
projects = {}
with open("res/project_list.json") as f:
    projects_json = json.loads(f.read())
for project_json in projects_json:
    p = project( project_json )
    projects[project_json["name"]] = p

#Init nodes and groups
nodes = ccetc_py.info.nodes()
groups = ccetc_py.info.groups()

def getProject(project):
    '''If it exists, returns project. Else, returns None'''
    if project in projects: return projects[project]
    else: return None

def getNode(node):
    '''If it exists, returns node object. Else, returns None'''
    if node in nodes: return nodes[node]
    else: return None

def getGroup(group):
    '''If it exists, returns group dict. Else, returns empty dict'''
    if group in groups: return groups[group]
    else: return {}
