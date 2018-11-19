import kgx

t = kgx.RdfOwlTransformer()
t.parse('data/mondo.owl')

t = kgx.ObanRdfTransformer(t.graph)
t.parse('data/orphanet.ttl')

n = kgx.NeoTransformer(
    host='localhost',
    ports={'bolt' : '8087'},
    username='neo4j',
    password='password'
)

n.graph = t.graph
n.save_with_unwind()
