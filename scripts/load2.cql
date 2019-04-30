USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///clique_merged_edges.csv" AS row
MERGE (subject:`named thing` {id: row.subject})
MERGE (object:`named thing` {id: row.object})
MERGE (subject)-[e:`related to`]->(object)
SET e += row;

