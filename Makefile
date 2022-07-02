# simulate ci/cd

pipeline: analysis test requirements build

# stages

analysis: linting static-analysis security-analysis

test: unittest

deploy: build run

# jobs

requirements:
	pipenv lock -r > requirements.txt

linting:
	# stage: analysis
	pylint --django-settings-module=server server/*

static-analysis:
	# stage: analysis
	bandit -r server -x tests

security-analysis:
	# stage: analysis
	safety check --full-report

unittest:
	# stage: test
	pytest server

backup:
	# stage: deploy
	docker cp authentication_system:/app/server/db.sqlite3 ./server/db.sqlite3
	docker exec authentication_system sha1sum /app/server/db.sqlite3
	sha1sum ./server/db.sqlite3

build:
	# stage: deploy
	docker build -t authentication_system:latest .
	docker images authentication_system:latest

	# init only
	# mkdir -p /etc/ssl/authentication.system
	# openssl genrsa -out /etc/ssl/authentication.system/private.pem 2048
	# openssl rsa -in /etc/ssl/authentication.system/private.pem -pubout -out /etc/ssl/authentication.system/public.pem

run:
	# stage: deploy
	docker run -d --restart always \
		--name authentication_system \
		-p 8500:8000 \
		-v /etc/ssl/authentication.system:/etc/ssl/authentication.system \
		authentication_system:latest

kill:
	docker stop authentication_system
	docker rm authentication_system

rebuild: build kill run
