up: 
	docker-compose up

up-blocked:
	docker-compose -f docker-compose-blocked.yml up

down: 
	docker-compose down

build: 
	docker-compose build

shell:
	docker exec -it feature_backend /bin/bash

block:
	docker exec -it feature_backend /bin/bash -c 'echo "127.0.0.1\tedge.api.flagsmith.com" >> /etc/hosts'

unblock:
	docker exec -it feature_backend /bin/bash -c 'sed "/127\.0\.0\.1\tedge\.api\.flagsmith\.com/d" /etc/hosts > /tmp/hosts.tmp'
	docker exec -it feature_backend /bin/bash -c 'cp /tmp/hosts.tmp /etc/hosts'
