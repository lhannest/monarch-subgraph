from kgx import ObanRdfTransformer, JsonTransformer, HgncRdfTransformer

t = ObanRdfTransformer()
t.add_ontology('data/mondo.owl')
t.add_ontology('data/hp.owl')
t.parse('data/hpoa.ttl')
t = JsonTransformer(t)
t.save('hpoa.json')
