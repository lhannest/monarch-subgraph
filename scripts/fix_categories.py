from kgx import ObanRdfTransformer, JsonTransformer

import click, bmt

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, type=click.Path(exists=False))
@click.option('--model', '-m', type=str, help='A URL or path to a biolink-model.yaml file')
def main(path, output, model):
    if model is not None:
        bmt.load(model)

    t = JsonTransformer()
    t.parse(path)

    def curie_to_label(curie:str):
        """
        Uses the biolink model toolkit to look up an
        element (on the tree rooted at `named thing`
        and `related to`) for a given curie. If none
        can be found then returns the original curie.
        """
        if isinstance(curie, (list, tuple, set)):
            return [curie_to_label(c) for c in curie]
        elif isinstance(curie, str):
            e = bmt.get_by_mapping(curie)
            return e if e is not None else curie
        else:
            return None

    for n, attr in t.graph.nodes(data=True):
        attr['category'] = curie_to_label(attr.get('category'))

    for s, o, attr in t.graph.edges(data=True):
        attr['predicate'] = curie_to_label(attr.get('predicate'))

    t.save(output)


if __name__ == '__main__':
    main()

