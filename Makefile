.PHONY: help up down logs migrate migrations seed restart clean

up:
	docker-compose up -d

down:
	docker-compose down

migrations:
	docker-compose exec app alembic revision --autogenerate -m "$(name)"

migrate:
	docker-compose exec app alembic upgrade head

seed:
	docker-compose exec app python seed_data.py
