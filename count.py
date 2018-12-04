from collections import Counter, Hashable
from kgx import JsonTransformer
from pprint import pprint

path = sys.argv[1]

t = JsonTransformer()
t.parse(path)

category_list = []

for n in t.graph.nodes():
    c = t.graph.node[n].get('category', ['named thing'])

    if isinstance(c, (list, tuple, set)):
        category_list.extend(c)
    else:
        category_list.append(c)

counter = Counter(category_list)

pprint(counter)

kmap = []
for s, o, attr in t.graph.edges(data=True):
    subject_categories = t.graph.node[s].get('category', ['named thing'])
    object_categories = t.graph.node[o].get('category', ['named thing'])
    predicates = attr.get('predicate', ['related to'])

    for subject_category in subject_categories:
        for object_category in object_categories:
            for predicate in predicates:
                kmap.append((subject_category, predicate, object_category))

counter = Counter(kmap)

pprint(counter)
