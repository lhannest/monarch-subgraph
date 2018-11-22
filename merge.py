import rdflib, sys, os, click

@click.command()
@click.option('--input', '-i', multiple=True, required=True, help='Path to an owl ontology file')
@click.option('--output', '-o', required=True, help='The path of the output file')
def merge(input, output):
    """
    Takes a series of xml files, and merges them into a single ttl file
    """
    for path in input:
        try:
            with open(path) as f:
                pass
        except:
            quit('Could not open {}'.format(path))
    try:
        with open(output, 'w+') as f:
            pass
    except:
        quit('Could not open {}'.format(path))

    graph = rdflib.Graph()

    for path in input:
        fmt = rdflib.util.guess_format(path)
        graph.parse(path, format=fmt)
        click.echo('[INFO]', path, len(graph))

    graph.serialize(destination=output, format='turtle')

if __name__ == '__main__':
    merge()


# if __name__ == '__main__':
#     def parse(graph, path):
#         fmt = rdflib.util.guess_format(path)
#         graph.parse(path, format=fmt)
#         print(path, len(graph))
#
#     try:
#         ttl_file = sys.argv[1]
#         owl_file = sys.argv[2]
#         outpath = sys.argv[3]
#     except:
#         quit('Usage: TTL OWL OUTPATH')
#
#     try:
#         with open(outpath, 'w') as f:
#             pass
#     except:
#         quit('Could not edit file {}'.format(outpath))
#
#     graph = rdflib.Graph()
#     parse(graph, 'data/orphanet.ttl')
#     parse(graph, 'data/mondo.owl')
#     graph.serialize(destination=outpath, format='turtle')
