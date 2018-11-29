from kgx import ObanRdfTransformer, JsonTransformer

# t = ObanRdfTransformer()
# t.add_ontology('data/mondo.owl')
# t.parse('data/orphanet.ttl')
# t = JsonTransformer(t)
# t.save('orphanet.json')

t = ObanRdfTransformer()
t.add_ontology('data/hp.owl')
t.parse('data/hpoa.ttl')
t = JsonTransformer(t)
t.save('hpoa.json')

# t = ObanRdfTransformer()
# # t.add_ontology('data/mondo.owl')
# t.parse('data/omim.ttl')
# t = JsonTransformer(t)
# t.save('omim.json')

t = ObanRdfTransformer()
t.add_ontology('data/go.owl')
t.add_ontology('data/so.owl')
t.parse('data/clinvar.ttl')
t = JsonTransformer(t)
t.save('clivar.json')
