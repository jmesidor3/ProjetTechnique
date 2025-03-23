.PHONY: setup test clean run start exec
# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help
SUBDIRS = wsgi
# Variables
VENV = .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
COVERAGE := $(VENV)/bin/coverage
help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make setup"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "------------------------------------"
clean: clean-build clean-pyc
	

flake8: 
	cd wsgi && ($(PYTHON) -m flake8 --extend-ignore E203,W234,E225,E501,E902 --output-file=flake8_report.txt biblio/templates)

# Créez l'environnement virtuel
$(VENV):
	( \
        python3 -m venv $(VENV); \
		source ./$</bin/activate ; set -u ;\
        $(PIP) install --upgrade pip; \
		$(PIP) install -r requirements.txt; \
        $(PIP) install coverage flake8 flake8-html pytest pdoc3; \
	)

test-coverage: ## Cleanup and deactivate venv
	cd wsgi && $(MAKE) test

test: ## Run pytest
	@docker exec biblio_app pytest . --junitxml=/app/pytest.xml
	@docker cp biblio_app:/app/pytest.xml ./pytest.xml

docs:  
	cd wsgi && $(PYTHON) -m pdoc --force --output-dir docs biblio/templates 
	@docker cp biblio_app:$(DOCS_DIR) ./docs

setup: destroy ## sets up environment and installs requirements
	@docker compose up -d

coverage-check: ## Create docker image
	@docker exec biblio_app coverage run -m pytest .
	@docker exec biblio_app coverage xml -o /app/coverage.xml
	@docker cp biblio_app:/app/coverage.xml ./coverage.xml
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: # type: ignore
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
 
destroy: ## build, start and run docker image
	@docker compose down --remove-orphans --volumes --rmi=local
	#@docker stop $(docker ps -q)
	#@docker network rm -f front_network back_network
	# docker rmi -f nginx:1.25.3
	# docker rmi -f biblio_app:1.0 
	# docker rmi -f redis:7.2.4
	# docker rmi -f mysql:8.0.22
	@docker volume rm -f mysql_volume
	@docker system prune -f
deploy: ## deploy the app with helm "helm append"