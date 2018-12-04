from kgx import ObanRdfTransformer, JsonTransformer
from collections import Counter

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

pprint(Counter([t.graph.node[n]['category'] for n in t.graph.nodes()]))
pprint(Counter([(t.graph.node[s]['category'], attr['predicate'], t.graph.node[o]['category']) for s, o, attr in t.graph.edges(data=True)]))
