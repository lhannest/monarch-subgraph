"""
Performs the last part of what main.py does.
"""

from kgx import JsonTransformer, PandasTransformer, clique_merge

t = JsonTransformer()
t.parse('hgnc.json')
t.parse('clinvar.json')
t.parse('omim.json')
t.parse('hpoa.json')
t.parse('orphanet.json')

t = PandasTransformer(t.graph)
t.parse('edges.csv')
t.parse('nodes.csv')

t.graph = clique_merge(t.graph)
t.save('clique_merged.csv')
