clone_webapp:
	@echo "${SUCCESS}✔${NC} Clone Project bothub-webapp"
	@git clone -b develop https://github.com/Ilhasoft/bothub-webapp.git bothub-webapp

engine_migration:
    @echo "Running Migrations"
    @docker exec -ti bothub_bothub.1.$(docker service ps -f 'name=bothub_bothub' bothub_bothub -q --no-trunc | head -n1) python manage.py migrate


engine_fakedata:
    @echo "Running fill database using fake data"
    @docker exec -ti bothub_bothub.1.$(docker service ps -f 'name=bothub_bothub' bothub_bothub -q --no-trunc | head -n1) python manage.py fill_db_using_fake_data
