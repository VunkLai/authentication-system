# simulate ci/cd

pipeline: analysis test

# stages

analysis: linting static-analysis security-analysis

test: unittest

build:

# jobs

requirements:
	pipenv lock -r > requirements.txt

linting:
	# stage: analysis
	pylint --django-settings-module=server server/*

static-analysis:
	# stage: analysis
	bandit -r server

security-analysis:
	# stage: analysis
	safety check --full-report

unittest:
	# stage: test
	pytest server
