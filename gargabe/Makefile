.PHONY: debut 
.PHONY: run clean

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

$(VENV):
	( \
        python3 -m venv $(VENV); \
		source ./$</bin/activate ; set -u ;\
        $(PIP) install --upgrade pip; \
		$(PIP) install -r requirements.txt; \
		python3 aiops/extract.py; \        
	)

venv: clean
	@echo "Creating a new virtual environment..."
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate
	@echo "Virtual environment rejuvenated."

extract: 
	@echo 'extract'
# extract: $(VENV)
# 	$(PYTHON) aiops/extract.py;
	

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

# setup: destroy
# 	@docker compose up -d --build
setup:
	@echo 'setup'
# trafic:
# 	bash request-script.sh
trafic:
	@echo 'trafic'
run: 
	python3 aiops/extract.py;	

traitement:
	@echo 'traitement'

encodage:
	@echo 'encodage'

generation:
	@echo 'generation'

training:
	@echo 'generation'

evaluation:
	@echo 'generation'

destroy: ## build, start and run docker image
	@docker compose down --remove-orphans --volumes --rmi=local
	#@docker stop $(docker ps -q)
	#@docker network rm -f front_network back_network
	# docker rmi -f nginx:1.25.3
	# docker rmi -f wsgi0:1.0  wsgi1:1.0 wsgi2:1.0
	# docker rmi -f redis:7.2.4
	# docker rmi -f mysql:8.0.22
	@docker volume rm -f mysql_volume
	@docker system prune -f
