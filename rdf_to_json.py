from kgx import ObanRdfTransformer, JsonTransformer
from collections import Counter

#o = ObanRdfTransformer()
#o.add_ontology('data/mondo.owl')
#o.add_ontology('data/hp.owl')
#o.add_ontology('data/go.owl')
#o.add_ontology('data/so.owl')
#o.add_ontology('data/ordo.owl')

from rdflib import URIRef

class HgncRdfTransformer():
    def add_node_attribute(node:str, key:str, value:str) -> None:
        if node in self.graph:
            attr_dict = self.graph.node[node]
            if key in attr_dict:
                attr_dict[key].append(value)
            else:
                attr_dict[key] = [value]
        else:
            self.graph.add_node(node, **{key : [value]})

    def load_edges(self, rdfgraph:rdflib.Graph, provided_by:str=None):
        for s, p, o in rdfgraph.triples((None, None, None)):
            s, p, o = str(s), str(p), str(o)

            if p == 'http://purl.obolibrary.org/obo/IAO_0000136':
                self.add_node_attribute(o, 'publications', s)
            elif p == 'http://purl.obolibrary.org/obo/RO_0002524':
                self.graph.add_edge(s, o, predicate='has_subsequence')
            else p == 'http://purl.obolibrary.org/obo/RO_0002525':
                self.graph.add_edge(o, s, predicate='has_subsequence')

t = HgncRdfTransformer()
t.parse('data/hgnc.ttl')
t = JsonTransformer(t)
t.save('hgnc.json')
quit()

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
