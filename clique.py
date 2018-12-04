from kgx import JsonTransformer, clique_merge
import sys

path = sys.argv[1]

t = JsonTransformer()
t.parse(path)

t.graph = clique_merge(t.graph)

t.save('clique_merged.json')
