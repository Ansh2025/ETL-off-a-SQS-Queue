pip-install:
	pip install -r requirements.txt
start:
	docker-compose up -d
stop:
	docker-compose down --remove-orphans
run:
	python process.py