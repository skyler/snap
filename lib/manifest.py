import re
import functools
import itertools

def combine_lines(lines,line):
    if lines and lines[-1] and lines[-1][-1] == '\\':
        lines[-1] = lines[-1][:-1] + line
    else:
        lines.append(line)
    return lines

def combine_quotes(items,item):
    if items and items[-1][0] == '"' \
             and (items[-1][-1] != '"' \
             or (len(items[-1]) > 2 and items[-1][-2] == '\\')):
        items[-1] = items[-1] + " " + item
    else:
        items.append(item)
    return items

def remove_enclosing_quotes(item):
    if item[0] == '"' and len(item) > 1 and item[-1] == '"':
        return item[1:-1]
    else:
        return item

def split_line(line):
    items = functools.reduce(combine_quotes,
                             re.findall('[^ ]+',line),
                             [])
    return list(map(remove_enclosing_quotes, items))

def parse_manifest(lines):
    '''Returns the lines of the manifest as a list of tuples. Possible tuples:

    ("stage",["filedir1","filedir2","...")
    ("local-script","script_name")
    ("remote-script","script_name")
    ("choice", ("choice description", {"choice1": <manifest tuple>, "choice2": <...>, ...}))
    ("pass",None)

    '''
    manifest = []

    lines = functools.reduce(combine_lines,lines,[])

    for line in lines:
        sline = split_line(line)
        if sline:
            parsed = parse_items(sline)
            manifest.append(parsed)

    return manifest

def parse_items(sline):
    command = sline[0]
    if len(sline) > 1:
        return command,parse_command_args(command,sline[1:])
    else:
        return command,None

def parse_command_args(command,args):
    if command == "stage":
        stages = list(map(lambda x: x.strip(), args))
        return stages

    elif command == "local-script":
        return args[0].strip()

    elif command == "remote-script":
        return args[0].strip()

    elif command == "choice":
        title = args[0]
        choices_raw = args[1:]
        choices_split = [list(x[1]) for x in itertools.groupby(choices_raw,lambda x: x == '|') if not x[0]]
        choices = {}
        for choice in choices_split:
            choices[choice[0]] = parse_items(choice[1:])

        return title,choices
