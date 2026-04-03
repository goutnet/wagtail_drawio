# Wagtail DrawIO - A Wagtail plugin to embed DrawIO diagrams in Wagtail pages

PROJECT=wagtail_drawio

BUILD=build
OUT=out

TESTENV=webroot

help:
	@echo "make env          : create the environment from the requirements.txt"
	@echo "make requirements.txt: update the requirements.txt"
	@echo "make update-env   : update the environment from requirements.txt"
	@echo "make test         : run the test suite with coverage"
	@echo "make coverage     : generate HTML coverage report (after make test)"
	@echo "make lint         : run black formatter"
	@echo "make webtest      : launch the test webserver"
	@echo "make freshdb      : recreate the test database and superuser"
	@echo "make dist         : build the package (sdist + wheel)"
	@echo "make clean/distclean"

.PHONY: FORCE

# Update the requirements.txt file with the current versions of the installed packages
# Will not touch the dependencies marked as >= or <=
requirements.txt: FORCE
	@echo "Updating requirements.txt (ignoring >= and <= dependencies), please change those to == if needed"
	@( \
		PATTERN=$$(cat requirements.txt | grep -v "^-e\|^#\|>=\|<=" | sed -e 's/[=><].*//' | tr '\n' '|' | sed 's/|/==\\|/g;s/\\|$$//') ; \
		tmpfile=$$(mktemp) ; \
		cat requirements.txt | grep -v "^-e\|^#" |grep '>=\|<=' > $${tmpfile} ; \
		if [ -n "$${PATTERN}" ]; then \
			pip freeze | grep -v "^-e\|^#" | grep "$${PATTERN}" >> ${{tmpfile}}; \
		fi; \
		diff -Naur requirements.txt $${tmpfile} || true ; \
		mv -f $${tmpfile} requirements.txt ; \
	)
	@echo "... requirements.txt updated"

env:
	mkdir -p env
	virtualenv --prompt="$(PROJECT)" -p python3 env
	( . env/bin/activate; pip install -r requirements.txt; pip install -r requirements-dev.txt )


update-env: FORCE
	( . env/bin/activate; pip install -r requirements.txt; pip install -r requirements-dev.txt )

.PHONY: webtest
webtest:
	cd $(TESTENV); ./manage.py runserver localhost:8000


.PHONY: freshdb
freshdb: clean_database
	cd $(TESTENV); ./manage.py makemigrations
	cd $(TESTENV); ./manage.py migrate
	cd $(TESTENV); echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'admin')" | python manage.py shell


.PHONY: clean
clean:
	rm -rf src/dist
	find . -iname '*.pyc' -delete
	rm -rf src/$(PROJECT).egg-info src/build

.PHONY: clean_migrations
clean_migrations:
	- for x in $(PROJECT)/migrations/*.py; do \
	    if [ -z "$$(git ls-files $$x )" ]; then \
		echo "removing $$x"; \
		rm -f $$x; \
	    fi; \
	   rm -rf $(PROJECT)/migrations/__pycache__; \
	done

.PHONY: clean_database
clean_database: clean_migrations
	rm -rf $(TESTENV)/db.sqlite3

.PHONY: distclean
distclean: clean clean_database
	rm -rf env

.PHONY: lint
lint:
	( . env/bin/activate; black . )

.PHONY: dist
dist: env
	mkdir -p $(OUT)
	( . env/bin/activate ; python -m build --outdir=$(OUT) )

.PHONY: test
test:
	( . env/bin/activate; PYTHONPATH=. pytest --ds=tests.test_settings --cov=$(PROJECT) --cov-report=term-missing tests/ )

.PHONY: coverage
coverage:
	( . env/bin/activate; coverage html )
