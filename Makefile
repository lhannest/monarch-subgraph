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

run:
	kgx neo4j-upload \
	--use-unwind \
	--scheme bolt \
	--port 8087 \
	-u neo4j \
	-p password \
	--host localhost \
	--node-property source_orphanet True \
	--edge-property source_orphanet True \
	data/orphanet.ttl

	kgx neo4j-upload \
	--use-unwind \
	--scheme bolt \
	--port 8087 \
	-u neo4j \
	-p password \
	--host localhost \
	--node-property source clinvar \
	--edge-property source clinvar \
	data/clinvar.ttl

	kgx neo4j-upload \
	--use-unwind \
	--scheme bolt \
	--port 8087 \
	-u neo4j \
	-p password \
	--host localhost \
	--node-property source hpoa \
	--edge-property source hpoa \
	data/hpoa.ttl

	kgx neo4j-upload \
	--use-unwind \
	--scheme bolt \
	--port 8087 \
	-u neo4j \
	-p password \
	--host localhost \
	--node-property source omim \
	--edge-property source omim \
	data/omim.ttl
