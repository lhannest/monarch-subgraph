import rdflib, sys, os

def parse(graph, path):
    fmt = rdflib.util.guess_format(path)
    graph.parse(path, format=fmt)


if __name__ == '__main__':
    try:
        outpath = sys.argv[1]
    except:
        quit('Usage: python rdf.py OUTPATH')

    try:
        with open(outpath, 'w') as f:
            pass
    except:
        quit('Could not edit file {}'.format(outpath))


    graph = rdflib.Graph()
    parse(graph, 'data/orphanet.ttl')
    parse(graph, 'data/mondo.owl')
    graph.serialize(destination=outpath, format='turtle')
