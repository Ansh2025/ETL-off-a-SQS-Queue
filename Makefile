pip-install:
	pip install -r requirements.txt
create:
	set PGPASSWORD=postgres
	psql -d postgres -U postgres -p 5432 -h localhost -f createtable.sql
start:
	docker-compose up -d
stop:
	docker-compose down --remove-orphans
run:
	python process.py
