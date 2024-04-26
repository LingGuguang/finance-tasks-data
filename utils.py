import json 

def read_json(path,encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        ret = json.load(f)
    return ret

def save_json(path, dic):
    with open(path,"w", encoding='utf-8') as f: 
        f.write(json.dumps(dic,ensure_ascii=False, indent=2)) 


def pprint(*args, **kwargs):
    return
    print(*args, **kwargs)

