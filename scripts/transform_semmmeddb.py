from kgx import ObanRdfTransformer, PandasTransformer
import networkx as nx
import pandas as pd

def load_edges(g:nx.Graph):
    # http://34.229.55.225/edges_neo4j.csv

    #SEMMED_PRED,pmids,negated,:TYPE,:START_ID,:END_ID,n_pmids,is_defined_by,relation,provided_by
    #AFFECTS,20801151,False,affects,UMLS:C1412045,UMLS:C0023946,1,semmeddb,semmeddb:affects,semmeddb_sulab
    #AFFECTS,19789049,False,affects,UMLS:C1412045,UMLS:C0028754,1,semmeddb,semmeddb:affects,semmeddb_sulab
    #AFFECTS,1409557,False,affects,UMLS:C1412045,UMLS:C0597304,1,semmeddb,semmeddb:affects,semmeddb_sulab
    #AFFECTS,7617239,False,affects,UMLS:C1412045,UMLS:C0599816,1,semmeddb,semmeddb:affects,semmeddb_sulab

    df = pd.read_csv('data/edges_neo4j.csv')

    def process_row(row):
        p = row['pmids']
        p = ['PMID:' + i for i in p.split(';')] if p is not None else None

        kwargs = dict(
                semmedPredicate=row['SEMMED_PRED'],
                pmids=p,
                n_pmids=row['n_pmids'],
                negated=row['negated'],
                predicate=row[':TYPE'],
                defined_by=row['is_defined_by'],
                provided_by=row['provided_by'],
                relation=row['relation']
        )

        g.add_edge(row[':START_ID'], row[':END_ID'], **kwargs)


    df.apply(process_row, axis=1)

def load_nodes(g:nx.Graph):
#:ID,name:STRING,umls_type:STRING[],umls_type_label:STRING[],:LABEL,xrefs:STRING[],category:STRING,id:STRING
#UMLS:C0061133,gastrin releasing peptide (14-27),T116,"Amino Acid, Peptide, or Protein",protein,MESH:C041922,protein,UMLS:C0061133
#UMLS:C1523610,"regulation of tube length, open tracheal system",T042,Organ or Tissue Function,biological_process_or_activity,GO:GO:0035159,biological_process_or_activity,UMLS:C1523610

    df = pd.read_csv('data/nodes_neo4j.csv')

    def process_row(row):
        xrefs = row['xrefs:STRING[]']
        xrefs = [xref for xref in xrefs.split(';')]
        kwargs = dict(
                name=row['name:STRING'],
                type=row['umls_type:STRING[]'],
                umls_type=row['umls_type_label:STRING[]'],
                label=row[':LABEL'],
                same_as=xrefs,
                category=row['category:STRING'],
                id=row['id:STRING']
        )

        n = row[':ID']

        if n in g:
            for key, value in kwargs.items():
                g.node[n][key] = value
        else:
            g.add_node(n, **kwargs)


    df.apply(process_row, axis=1)


if __name__ == '__main__':
    g = nx.Graph()
    t = PandasTransformer()
    load_nodes(t.graph)
    load_edges(t.graph)
    t.save('semmeddb.csv')
