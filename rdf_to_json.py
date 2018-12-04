from kgx import ObanRdfTransformer, JsonTransformer
from collections import Counter
from pprint import pprint

t = ObanRdfTransformer()
t.add_ontology('data/mondo.owl')
t.parse('data/orphanet.ttl')
t = JsonTransformer(t)
t.save('orphanet.json')

t = ObanRdfTransformer()
t.add_ontology('data/hp.owl')
t.parse('data/hpoa.ttl')
t = JsonTransformer(t)
t.save('hpoa.json')

t = ObanRdfTransformer()
t.parse('data/omim.ttl')
t = JsonTransformer(t)
t.save('omim.json')

t = ObanRdfTransformer()
t.add_ontology('data/go.owl')
t.add_ontology('data/so.owl')
t.parse('data/clinvar.ttl')
t = JsonTransformer(t)
t.save('clinvar.json')

t = JsonTransformer()
t.parse('clinvar.json')
t.parse('omim.json')
t.parse('hpoa.json')
t.parse('orphanet.json')

for n in t.graph.nodes():
    attr = t.graph.node[n]
    if 'category' not in attr:
        attr['category'] = ['named thing']

for s, o, attr in t.graph.edges(data=True):
    if 'predicate' not in attr:
        attr['predicate'] = ['related to']

t.save('merged.json')

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
