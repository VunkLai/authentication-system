all:
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

check: linting static-analysis security-analysis
	# stage: linting static-analysis security-analysis
