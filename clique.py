from kgx import JsonTransformer, clique_merge
import sys

path = sys.argv[1]
output = sys.argv[2]

t = JsonTransformer()
t.parse(path)

t.graph = clique_merge(t.graph)

t.save(output)
