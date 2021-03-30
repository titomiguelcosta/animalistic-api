lint:
	flake8

lintstats:
	flake8 --statistics --count -qq

lintfix:
	autopep8 --aggressive -i -r --max-line-length=100 fusebox

.PHONY: tests
tests:
	cd fusebox && python manage.py test --noinput

.PHONY: deploy
deploy:
	php bin/dep deploy dev
