from kgx import ObanRdfTransformer, JsonTransformer
from collections import Counter

o = ObanRdfTransformer()
o.add_ontology('data/mondo.owl')
o.add_ontology('data/hp.owl')
o.add_ontology('data/go.owl')
o.add_ontology('data/so.owl')
o.add_ontology('data/ordo.owl')

t = ObanRdfTransformer()
t.ontologies = o.ontologies
t.parse('data/orphanet.ttl')
t = JsonTransformer(t)
t.save('orphanet.json')

t = ObanRdfTransformer()
t.ontologies = o.ontologies
t.parse('data/hpoa.ttl')
t = JsonTransformer(t)
t.save('hpoa.json')

t = ObanRdfTransformer()
t.ontologies = o.ontologies
t.parse('data/omim.ttl')
t = JsonTransformer(t)
t.save('omim.json')

t = ObanRdfTransformer()
t.ontologies = o.ontologies
t.parse('data/clinvar.ttl')
t = JsonTransformer(t)
t.save('clinvar.json')

t = JsonTransformer()
t.parse('clinvar.json')
t.parse('omim.json')
t.parse('hpoa.json')
t.parse('orphanet.json')
t.save('merged.json')
