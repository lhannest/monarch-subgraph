from collections import Counter, Hashable
from kgx import JsonTransformer
from pprint import pprint
import sys

if len(sys.argv) < 1:
    quit('Required argument: path to json knowledge graph')

path = sys.argv[1]

t = JsonTransformer()
t.parse(path)

category_list = []
uncategorized_example = {}
uncategorized_frequency = {}
for n in t.graph.nodes():
    c = t.graph.node[n].get('category')

    if c is None:
        iri = t.graph.node[n].get('iri')
        k = iri.split('/')
        if '_' in k[-1]:
            prefix, _ = k[-1].split('_', 1)
            k = tuple(k[:-1] + [prefix])
        else:
            k = tuple(k[:-1])

        if k not in uncategorized_example:
            uncategorized_example[k] = iri
            uncategorized_frequency[k] = 1
        else:
            uncategorized_frequency[k] += 1

    if isinstance(c, (list, tuple, set)):
        category_list.extend(c)
    else:
        category_list.append(c)

print('Examples of uncategorized nodes:')
for key, value in uncategorized_example:
    print('/'.join(key), '\t', value, '\t', uncategorized_frequency[key])

print('Categories:')
counter = Counter(category_list)
pprint(counter)

kmap = []
for s, o, attr in t.graph.edges(data=True):
    subject_categories = t.graph.node[s].get('category', [None])
    object_categories = t.graph.node[o].get('category', [None])
    predicates = attr.get('predicate', [None])

    if not isinstance(subject_categories, (list, tuple, set)):
        subject_categories = [subject_categories]

    if not isinstance(object_categories, (list, tuple, set)):
        object_categories = [object_categories]

    if not isinstance(predicates, (list, tuple, set)):
        predicates = [predicates]

    for subject_category in subject_categories:
        for object_category in object_categories:
            for predicate in predicates:
                kmap.append((subject_category, predicate, object_category))

print('Knowledge Map:')
counter = Counter(kmap)
pprint(counter)
