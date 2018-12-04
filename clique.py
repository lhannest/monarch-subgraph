import networkx as nx

def relabel_nodes(graph:nx.Graph, mapping:dict) -> nx.Graph:
    """
    Performs the relabelling of nodes, and ensures that list properties are
    copied over.

    import networkx as nx

    graph = nx.Graph()

    graph.add_edge('a', 'b')
    graph.add_edge('c', 'd')
    graph.node['a']['name'] = ['A']
    graph.node['b']['name'] = ['B']
    graph.node['c']['name'] = ['C']
    graph.node['d']['name'] = ['D']

    graph = relabel_nodes(graph, {'c' : 'b'})

    for n in graph.nodes():
        print(n, graph.node[n])
    """
    g = nx.relabel_nodes(graph, mapping, copy=True)

    for n in g.nodes():
        d = g.node[n]
        attr = graph.node[n]

        for key, value in attr.items():
            if key in d:
                if isinstance(d[key], (list, set, tuple)) and isinstance(attr[key], (list, set, tuple)):
                    s = set(d[key])
                    s.update(attr[key])
                    d[key] = list(s)
            else:
                d[key] = value
    return g

import networkx as nx

graph = nx.Graph()

graph.add_edge('a', 'b')
graph.add_edge('c', 'd')
graph.node['a']['name'] = ['A']
graph.node['b']['name'] = ['B']
graph.node['c']['name'] = ['C']
graph.node['d']['name'] = ['D']

graph = relabel_nodes(graph, {'c' : 'b'})

for n in graph.nodes():
    print(n, graph.node[n])

quit()

from kgx import JsonTransformer, clique_merge

t = JsonTransformer()
t.parse('merged.json')

t.graph = clique_merge(t.graph)

t.save('clique_merged.json')


for n in t.graph.nodes():
    attr = t.graph.node[n]
    if 'category' not in attr:
        attr['category'] = ['named thing']

for s, o, attr in t.graph.edges(data=True):
    if 'predicate' not in attr:
        attr['predicate'] = ['related to']

t.save('merged.json')

category_list = []

for n in t.graph.nodes():
    c = t.graph.node[n].get('category', ['named thing'])

    if isinstance(c, (list, tuple, set)):
        category_list.extend(c)
    else:
        category_list.append(c)

counter = Counter(category_list)

pprint(counter)

kmap = []
for s, o, attr in t.graph.edges(data=True):
    subject_categories = t.graph.node[s].get('category', ['named thing'])
    object_categories = t.graph.node[o].get('category', ['named thing'])
    predicates = attr.get('predicate', ['related to'])

    for subject_category in subject_categories:
        for object_category in object_categories:
            for predicate in predicates:
                kmap.append((subject_category, predicate, object_category))

counter = Counter(kmap)

pprint(counter)
