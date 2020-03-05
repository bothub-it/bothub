docker exec -ti bothub_bothub.1.$(docker service ps -f 'name=bothub_bothub' bothub_bothub -q --no-trunc | head -n1) python manage.py migrate
