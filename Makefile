run:
	make download
	python scripts/transform_semmeddb.py
	tar -xvf semmeddb.csv.tar
	nohup python scripts/main.py &
	# tar -xvf semmeddb.csv.tar
	# Finally, unzip the resulting `clique_merged.csv` file and place `edges.csv`
	# and `nodes.csv` into neo4j/import, and use `monarch_load.cql` to load them.

download:
	mkdir data || echo "directory already exists"

	wget https://data.monarchinitiative.org/ttl/clinvar.ttl -O data/clinvar.ttl
	wget https://data.monarchinitiative.org/ttl/orphanet.ttl -O data/orphanet.ttl
	wget https://data.monarchinitiative.org/ttl/omim.ttl -O data/omim.ttl
	wget https://archive.monarchinitiative.org/latest/ttl/hpoa.ttl -O data/hpoa.ttl
	wget https://data.monarchinitiative.org/ttl/hgnc.ttl -O data/hgnc.ttl
	wget http://34.229.55.225/nodes_neo4j.csv -O data/semmeddb_nodes.csv
	wget http://34.229.55.225/edges_neo4j.csv -O data/semmeddb_edges.csv

	wget https://www.ebi.ac.uk/ols/ontologies/ordo/download -O data/ordo.owl
	wget http://purl.obolibrary.org/obo/mondo.owl -O data/mondo.owl
	wget https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.owl -O data/hp.owl
	wget https://raw.githubusercontent.com/The-Sequence-Ontology/SO-Ontologies/master/so.owl -O data/so.owl
	wget http://purl.obolibrary.org/obo/go.owl -O data/go.owl
	wget http://data.bioontology.org/ontologies/ORDO/submissions/14/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb -O ordo_orphanet.owl

env:
	# https://askubuntu.com/a/865644
	export PATH="~/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"

merge:
	python merge.py \
		-i data/orphanet.ttl \
		-i data/mondo.owl \
		-i data/hpoa.ttl \
		-i data/hp.owl \
		-o data/orphanet_hpoa.ttl

run:
	kgx neo4j-upload --use-unwind --scheme bolt --port 8087 -u neo4j -p password --host localhost --node-property source_orphanet True --edge-property orphanet_mondo yes data/out.ttl

docker:
	docker run \
		-d \
		--name monarch-neo4j \
		--env NEO4J_AUTH=neo4j/password \
		--publish=8086:7474 \
		--publish=8087:7687 \
		--volume=`pwd`/neo4j/data:/data \
		--volume=`pwd`/neo4j/logs:/logs \
		neo4j:3.0

# run:
# 	kgx neo4j-upload \
# 	--use-unwind \
# 	--scheme bolt \
# 	--port 8087 \
# 	-u neo4j \
# 	-p password \
# 	--host localhost \
# 	--node-property source_orphanet True \
# 	--edge-property source_orphanet True \
# 	data/orphanet.ttl
#
# 	kgx neo4j-upload \
# 	--use-unwind \
# 	--scheme bolt \
# 	--port 8087 \
# 	-u neo4j \
# 	-p password \
# 	--host localhost \
# 	--node-property source clinvar \
# 	--edge-property source clinvar \
# 	data/clinvar.ttl
#
# 	kgx neo4j-upload \
# 	--use-unwind \
# 	--scheme bolt \
# 	--port 8087 \
# 	-u neo4j \
# 	-p password \
# 	--host localhost \
# 	--node-property source hpoa \
# 	--edge-property source hpoa \
# 	data/hpoa.ttl
#
# 	kgx neo4j-upload \
# 	--use-unwind \
# 	--scheme bolt \
# 	--port 8087 \
# 	-u neo4j \
# 	-p password \
# 	--host localhost \
# 	--node-property source omim \
# 	--edge-property source omim \
# 	data/omim.ttl
