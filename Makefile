ENGINE_PORT ?= 8000


# Commands

install_requirements:
	@echo "${SUCCESS}✔${NC} Created Directory projects"
	@mkdir projects
	@echo "${SUCCESS}✔${NC} Clone Project bothub-webapp"
	@git clone https://github.com/Ilhasoft/bothub-webapp.git projects/bothub-webapp
	@echo "${SUCCESS}✔${NC} Clone Project bothub-engine"
	@git clone https://github.com/Ilhasoft/bothub-engine.git projects/bothub-engine
	@echo "${SUCCESS}✔${NC} Clone Project bothub-nlp"
	@git clone https://github.com/udomobi/bothub-nlp.git projects/bothub-nlp

	@echo "SUPPORTED_LANGUAGES=en:en_core_web_md|pt:pt" >> .env
	@echo "DEFAULT_DATABASE=postgres://bothub:bothub@database:5432/bothub" >> .env
	@echo "ENGINE_PORT=8000" >> .env

	@cp -a projects/bothub-nlp/bothub-nlp-nlu-worker/bothub_nlp_nlu_worker/bothub_nlp_celery/* projects/bothub-nlp/bothub-nlp-api/bothub_nlp_api/celerytasks/
	@echo "${SUCCESS}✔${NC} Created .env"

init_stack:
	@echo "${SUCCESS}✔${NC} Starting Build bothub-engine"
	@docker-compose -f projects/bothub-engine/docker-compose.yml build
	@docker-compose -f projects/bothub-engine/docker-compose.yml up -d
	@echo "${SUCCESS}✔${NC} Starting Build bothub-webapp"
	@docker-compose -f projects/bothub-webapp/docker-compose.yml build
	@docker-compose -f projects/bothub-webapp/docker-compose.yml up -d
	@echo "${SUCCESS}✔${NC} Starting Build bothub-nlp"
	@docker-compose -f projects/bothub-nlp/docker-compose.yml build --build-arg DOWNLOAD_SPACY_MODELS=en:en_core_web_md
	@docker-compose -f projects/bothub-nlp/docker-compose.yml up -d
	@echo "${SUCCESS}✔${NC} Finish"


destroy_stack:
	@echo "${SUCCESS}✔${NC} Destroying Build bothub-engine"
	@docker-compose -f projects/bothub-engine/docker-compose.yml down --rmi all
	@echo "${SUCCESS}✔${NC} Destroying Build bothub-webapp"
	@docker-compose -f projects/bothub-webapp/docker-compose.yml down --rmi all
	@echo "${SUCCESS}✔${NC} Destroying Build bothub-nlp"
	@docker-compose -f projects/bothub-nlp/docker-compose.yml down --rmi all
	@echo "${SUCCESS}✔${NC} Finish"


restart:
	@echo "${SUCCESS}✔${NC} Restart Build bothub-engine"
	@docker-compose -f projects/bothub-engine/docker-compose.yml down --rmi all
	@echo "${SUCCESS}✔${NC} Restart Build bothub-webapp"
	@docker-compose -f projects/bothub-webapp/docker-compose.yml down --rmi all
	@echo "${SUCCESS}✔${NC} Restart Build bothub-nlp"
	@docker-compose -f projects/bothub-nlp/docker-compose.yml restart
	@echo "${SUCCESS}✔${NC} Finish"



## Colors
SUCCESS = \033[0;32m
INFO = \033[0;36m
WARNING = \033[0;33m
DANGER = \033[0;31m
NC = \033[0m
