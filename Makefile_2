.PHONY: setup test clean run start exec
# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help
SUBDIRS = wsgi
# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make setup"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "------------------------------------"
clean: ## Remove build and cache files
	cd wsgi && $(MAKE) clean

flake8:
	cd wsgi && $(MAKE) lint

test-coverage: ## Cleanup and deactivate venv
	cd wsgi && $(MAKE) test

test: ## Run pytest
	cd wsgi && $(MAKE) test

docs: ## Build docker image
	cd wsgi && $(MAKE) docs

setup: run ## sets up environment and installs requirements
	$(MAKE) -C $(SUBDIRS) setup

coverage-check: ## Create docker image
	cd wsgi && $(MAKE) coverage-check
 
run: ## build, start and run docker image
	bash docker-mysql.sh
	cd wsgi && flask run
	# docker run -it --rm -dp 8080:80 -v "$(pwd)/configs:/etc/nginx/conf.d" --name biblio_nginx nginx
 

 