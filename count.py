from collections import Counter
from kgx import JsonTransformer
from pprint import pprint

t = JsonTransformer()
t.parse('clinvar.json')
categories = []
for n in t.graph.nodes():
    c = t.graph.node[n].get('category', None)
    categories.append(c)

d = Counter(categories)

pprint(d)

with open('count.txt', 'w+') as f:
    f.write(str(d))
