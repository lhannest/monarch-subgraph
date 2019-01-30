from kgx import ObanRdfTransformer, JsonTransformer, PandasTransformer

import click

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, type=click.Path(exists=False))
@click.option('--model', '-m', type=str, help='A URL or path to a biolink-model.yaml file')
def main(path, output, model):
    if model is not None:
        bmt.load(model)

    t = JsonTransformer()
    t.parse(path)
    t = PandasTransformer(t.graph)
    t.save(output)


if __name__ == '__main__':
    main()

