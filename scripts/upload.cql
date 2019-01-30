CREATE CONSTRAINT ON (n:`named thing`) ASSERT n.id IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///edges.csv" AS row
MERGE (subject:`named thing` {id: row.subject})
MERGE (object:`named thing` {id: row.object})
WITH DISTINCT subject, object, row
CALL apoc.create.relationship(subject, row.predicate, row, object) YIELD rel
RETURN COUNT(*);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///nodes.csv" AS row
MERGE (n:`named thing` {id: row.id})
WITH DISTINCT n, row, SPLIT(row.category, ';') AS categories
CALL apoc.create.addLabels(n, COALESCE(categories, [])) YIELD node
SET n += row
RETURN COUNT(*);

