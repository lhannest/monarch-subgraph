from kgx import ObanRdfTransformer, JsonTransformer, HgncRdfTransformer
from kgx import clique_merge

t = HgncRdfTransformer()
t.parse('data/hgnc.ttl')
t = JsonTransformer(t)
t.save('hgnc.json')

t = ObanRdfTransformer()
t.add_ontology('data/hp.owl')
t.parse('data/orphanet.ttl')
t = JsonTransformer(t)
t.save('orphanet.json')

t = ObanRdfTransformer()
t.parse('data/hpoa.ttl')
t = JsonTransformer(t)
t.save('hpoa.json')

t = ObanRdfTransformer()
t.add_ontology('data/mondo.owl')
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
t.save('merged.json')

t.graph = clique_merge(t.graph)
t.save('clique_merged.json')
