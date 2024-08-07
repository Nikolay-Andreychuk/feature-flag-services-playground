up: 
	docker-compose up -d

down: 
	docker-compose down

build: 
	docker-compose build

shell:
	docker exec -it feature_backend /bin/bash

block:
	docker exec -it feature_backend /bin/bash -c 'echo "127.0.0.1 api.feature-service.com" >> /etc/hosts'

unblock:
	docker exec -it feature_backend /bin/bash -c 'sed "/127\.0\.0\.1 api\.feature-service\.com/d" /etc/hosts > /tmp/hosts.tmp'
	docker exec -it feature_backend /bin/bash -c 'cp /tmp/hosts.tmp /etc/hosts'