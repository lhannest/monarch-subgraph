from kgx import ObanRdfTransformer, JsonTransformer, HgncRdfTransformer
from kgx import clique_merge

t = JsonTransformer()
#t.parse('hgnc.json')
#t.parse('clinvar.json')
#t.parse('omim.json')
#t.parse('hpoa.json')
#t.parse('orphanet.json')
t.parse('semmeddb.json')
t.parse('merged.json')
t.save('merged.json')

t.graph = clique_merge(t.graph)
t.save('clique_merged.json')
