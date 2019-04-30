from kgx import ObanRdfTransformer, JsonTransformer, HgncRdfTransformer
from collections import Counter

t = ObanRdfTransformer()
t.add_ontology('data/mondo.owl')
t.add_ontology('data/go.owl')
t.add_ontology('data/so.owl')
t.parse('data/clinvar.ttl')
t = JsonTransformer(t)
t.save('clinvar.json')

