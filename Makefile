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

neo4j-logs:
	docker logs ncats-monarch-graph-2019-01-25

neo4j-ssh:
	docker exec -it ncats-monarch-graph-2019-01-25 /bin/bash

neo4j-stop:
	docker stop ncats-monarch-graph-2019-01-25

neo4j-start:
	mkdir -p neo4j/plugins
	#wget --no-clobber https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.1/apoc-3.5.0.1-all.jar --directory-prefix=/work/neo4j/plugins
	wget --no-clobber https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.0.8.6/apoc-3.0.8.6-all.jar --directory-prefix=/work/neo4j/plugins
	echo `pwd`
	docker run \
		-d \
		--rm \
		--env NEO4J_dbms_memory_heap_maxSize=5120 \
		--name ncats-monarch-graph-2019-01-25 \
		-p 8086:7474 \
		-p 8088:7473 \
		-p 8087:7687 \
		-v /work/neo4j/plugins:/plugins \
		-v /work/neo4j/data:/data \
		-v /work/neo4j/conf:/var/lib/neo4j/conf \
		-v /work/neo4j/import:/var/lib/neo4j/import \
		neo4j:3.0


