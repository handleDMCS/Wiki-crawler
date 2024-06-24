import json

# display JSON data in a comprehensible way
def fetch(data):
    open_bracket = ['{', '[']
    close_bracket = ['}', ']']
    str = json.dumps(data).replace(' ', '')
    space = ''
    prev = False
    for c in str:
        if prev:
            if(c in open_bracket):
                print(f'\n{space}', end='')
                space += '  '
            elif(c in close_bracket):
                space = space[:-2]
                print(f'\n{space}', end='')
            else:
                if(prev in close_bracket) or (prev in open_bracket) or (prev == ','):
                    print(f'\n{space}', end='')
        print(c, end='')
        prev = c

# get a specific propety from a json object
def get_path(path, data):
    curr = data
    for step in path:
        if isinstance(step, str):
            curr = curr.get(step, False)
        else:
            try:
                curr = curr[step] 
            except:
                curr = False
        if not curr:
            break
    return curr