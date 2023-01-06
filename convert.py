import sys
import os
import json

import pdb

paths = "./data"
dirs = os.listdir(paths)

for _dir in dirs:
    fact_path = os.path.join(paths, _dir, 'facts_clingo.pl')
    quest_path = os.path.join(paths, _dir, 'quest_clingo.pl')
    text_path = os.path.join(paths, _dir, 'text_logic_form.json')
    diagram_path = os.path.join(paths, _dir, 'diagram_logic_form.json')

    open(fact_path, 'w').close()
    open(quest_path, 'w').close()

    fact_handle = open(fact_path, 'w')
    quest_handle = open(quest_path, 'w')    

    with open(text_path) as f:
        text_json = json.load(f)

    with open(diagram_path) as f:
        diagram_json = json.load(f)





pdb.set_trace()