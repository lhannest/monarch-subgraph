env:
	# https://askubuntu.com/a/865644
	export PATH="~/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"
test:
	cat `pwd`/out.json

docker:
	docker run \
		-d \
		--name monarch-neo4j \
		--env NEO4J_AUTH=neo4j/password \
		--publish=8086:7474 \
		--publish=8087:7687 \
		--volume=`pwd`/neo4j/data:/data \
		--volume=`pwd`/neo3j/logs:/logs \
		neo4j:3.0

run:
	kgx neo4j-upload \
	--use-unwind \
	--scheme bolt \
	--port 8087 \
	-u neo4j \
	-p password \
	--host localhost \
	--node-property source orphanet \
	--edge-property source orphanet \
	data/orphanet.ttl
	#data/clinvar.ttl \
	#data/hpoa.ttl \
	#data/omim.ttl
