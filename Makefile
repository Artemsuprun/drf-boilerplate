# ==================================================
# Configuration
# ==================================================

-include .env

COMPOSE_BASE = docker-compose.yml
COMPOSE_DEV = docker-compose.dev.yml
COMPOSE_PROD = docker-compose.prod.yml

PROJECT_NAME ?= app

DEV_PROJECT = $(PROJECT_NAME)-dev
PROD_PROJECT = $(PROJECT_NAME)-prod

DEV = docker compose -p $(DEV_PROJECT) -f $(COMPOSE_BASE) -f $(COMPOSE_DEV)
PROD = docker compose -p $(PROD_PROJECT) -f $(COMPOSE_BASE) -f $(COMPOSE_PROD)

.PHONY: dev dev-detached down-dev restart-dev reset-dev \
        prod deploy-prod down-prod restart-prod cert-init cert-renew-test \
        logs logs-backend logs-nginx logs-db logs-prod \
        migrate makemigrations createsuperuser shell collectstatic \
        migrate-prod collectstatic-prod createsuperuser-prod \
        reset-db reset-all


# ==================================================
# Development
# ==================================================

dev:
	$(DEV) up --build

dev-detached:
	$(DEV) up -d --build

down-dev:
	$(DEV) down

restart-dev:
	$(DEV) up -d --build --force-recreate

reset-dev:
	$(DEV) down -v


# ==================================================
# Production
# ==================================================

cert-init: ## FIRST DEPLOY ONLY: issue the Let's Encrypt cert (port 80 must be free, DNS must point here)
	$(PROD) run --rm --no-deps -p 80:80 --entrypoint certbot certbot certonly \
	  --standalone --non-interactive --agree-tos -m $(LETSENCRYPT_EMAIL) \
	  -d $(DOMAIN) -d www.$(DOMAIN)

cert-renew-test:
	$(PROD) run --rm --no-deps --entrypoint certbot certbot renew --dry-run --webroot -w /var/www/certbot

prod:
	$(PROD) up -d --build

deploy-prod:
	$(PROD) build
	$(MAKE) migrate-prod
	$(MAKE) collectstatic-prod
	$(PROD) up -d

down-prod:
	$(PROD) down

restart-prod:
	$(PROD) up -d --build --force-recreate


# ==================================================
# Logs
# ==================================================

logs:
	$(DEV) logs -f

logs-prod:
	$(PROD) logs -f

logs-backend:
	$(DEV) logs -f backend

logs-nginx:
	$(DEV) logs -f nginx

logs-db:
	$(DEV) logs -f db


# ==================================================
# Django commands (development)
# ==================================================

migrate:
	$(DEV) exec backend python manage.py migrate

makemigrations:
	$(DEV) exec backend python manage.py makemigrations

createsuperuser:
	$(DEV) exec backend python manage.py createsuperuser

shell:
	$(DEV) exec backend python manage.py shell

collectstatic:
	$(DEV) exec backend python manage.py collectstatic --noinput


# ==================================================
# Django commands (production)
# ==================================================

migrate-prod:
	$(PROD) run --rm backend python manage.py migrate --noinput

collectstatic-prod:
	$(PROD) run --rm backend python manage.py collectstatic --noinput

createsuperuser-prod:
	$(PROD) run --rm backend python manage.py createsuperuser


# ==================================================
# Database
# ==================================================

reset-db:
	$(DEV) down -v


# ==================================================
# Everything
# ==================================================

reset-all:
	$(DEV) down -v
	$(PROD) down -v
