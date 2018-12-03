from collections import Counter, Hashable
from kgx import JsonTransformer
from pprint import pprint

t = JsonTransformer()
t.parse('clinvar.json')
categories = []
for n in t.graph.nodes():
    c = t.graph.node[n].get('category', None)
    if isinstance(c, (list, tuple, set)):
        categories.extend(c)
    elif isinstance(c, Hashable)
        categories.append(c)
    else:
        categories.append('unhashable object: {}'.format(str(c)))

d = Counter(categories)

pprint(d)

with open('count.txt', 'w+') as f:
    f.write(str(d))
