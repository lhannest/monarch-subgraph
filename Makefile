env:
	# https://askubuntu.com/a/865644
	export PATH="~/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"
test:
	cat `pwd`/out.json

download:
	mkdir data || echo "directory already exists"
	wget https://data.monarchinitiative.org/ttl/clinvar.ttl -O data/clinvar.ttl
	wget https://data.monarchinitiative.org/ttl/orphanet.ttl -O data/orphanet.ttl
	wget https://data.monarchinitiative.org/ttl/omim.ttl -O data/omim.ttl
	wget https://archive.monarchinitiative.org/latest/ttl/hpoa.ttl -O data/hpoa.ttl

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


