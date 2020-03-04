clone_webapp:
	@echo "${SUCCESS}✔${NC} Clone Project bothub-webapp"
	@git clone -b develop https://github.com/Ilhasoft/bothub-webapp.git bothub-webapp

engine_migration:
	@echo "Running Migrations"
	@chmod +x migration.sh
	@sh migration.sh


engine_fakedata:
	@echo "Running fill database using fake data"
	@chmod +x fake_data.sh
	@sh fake_data.sh
