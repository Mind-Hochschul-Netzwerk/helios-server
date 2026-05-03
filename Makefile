# =============================================================================
# Makefile – Helios Voting Server
# Verwendung: make <target>
# =============================================================================

COMPOSE = docker compose
ENV_FILE = .env

# Farben
GREEN  = \033[0;32m
YELLOW = \033[1;33m
NC     = \033[0m

# .env prüfen (wird vor jedem Target ausgeführt das es braucht)
.check-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(YELLOW)[helios]$(NC) .env nicht gefunden!"; \
		echo "$(YELLOW)[helios]$(NC) Bitte zuerst ausführen: cp env.sample .env && nano .env"; \
		exit 1; \
	fi

# Datenverzeichnisse anlegen
.create-dirs: .check-env
	@DATA_DIR=$$(grep '^DATA_DIR=' $(ENV_FILE) | cut -d= -f2 | tr -d '"' | tr -d "'"); \
	if [ -n "$$DATA_DIR" ]; then \
		echo "$(GREEN)[helios]$(NC) Lege Datenverzeichnisse an: $$DATA_DIR"; \
		mkdir -p "$$DATA_DIR/postgres/db/16/data"; \
		mkdir -p "$$DATA_DIR/rabbitmq"; \
	fi

##@ Hauptbefehle

.PHONY: up
up: .check-env .create-dirs ## Alle Services starten (ohne Neubau)
	@echo "$(GREEN)[helios]$(NC) Starte Infrastruktur..."
	@$(COMPOSE) up -d database rabbitmq
	@echo "$(GREEN)[helios]$(NC) Warte auf PostgreSQL..."
	@until $(COMPOSE) exec -T database pg_isready -U user &>/dev/null; do sleep 1; done
	@echo "$(GREEN)[helios]$(NC) Warte auf RabbitMQ..."
	@until $(COMPOSE) exec -T rabbitmq sh -c 'rabbitmqctl status' &>/dev/null 2>&1; do sleep 2; done
	@echo "$(GREEN)[helios]$(NC) Führe Datenbankmigrationen aus..."
	@$(COMPOSE) run --rm app uv run python manage.py migrate --noinput
	@echo "$(GREEN)[helios]$(NC) Starte App und Worker..."
	@$(COMPOSE) up -d app worker
	@echo "$(GREEN)[helios]$(NC) ✅ Helios läuft: https://$$(grep '^SERVICENAME=' $(ENV_FILE) | cut -d= -f2).$$(grep '^DOMAINNAME=' $(ENV_FILE) | cut -d= -f2)"

.PHONY: build
build: .check-env ## Docker-Image neu bauen (nach git pull oder Dockerfile-Änderung)
	@echo "$(GREEN)[helios]$(NC) Baue Docker-Image..."
	@$(COMPOSE) build
	@echo "$(GREEN)[helios]$(NC) Build abgeschlossen."

.PHONY: rebuild
rebuild: build up ## Image neu bauen und danach starten

.PHONY: down
down: ## Alle Container stoppen und entfernen
	@echo "$(GREEN)[helios]$(NC) Stoppe alle Container..."
	@$(COMPOSE) down
	@echo "$(GREEN)[helios]$(NC) Fertig."

.PHONY: restart
restart: down up ## Alle Container neu starten

##@ Datenbank & Wartung

.PHONY: migrate
migrate: .check-env ## Datenbankmigrationen ausführen
	@$(COMPOSE) run --rm app uv run python manage.py migrate --noinput

.PHONY: createadmin
createadmin: .check-env ## Helios-Admin-Account anlegen (Passwort-Login)
	@bash -c '\
	read -p "Benutzername: " username; \
	read -p "E-Mail: " email; \
	read -s -p "Passwort: " password; \
	echo; \
	$(COMPOSE) exec app uv run python manage.py shell -c "\
from helios_auth.models import User; \
u = User.objects.create(user_id=\"$$username\", user_type=\"password\", info={\"password\": \"$$password\", \"email\": \"$$email\", \"name\": \"$$username\"}, admin_p=True); \
print(\"Helios-User erstellt:\", u.user_id)"'

.PHONY: shell
shell: .check-env
	@$(COMPOSE) exec app bash

.PHONY: dbshell
dbshell: .check-env ## PostgreSQL-Shell öffnen
	@$(COMPOSE) exec database psql -U user -d database

.PHONY: logs
logs: ## Logs aller Container (live)
	@$(COMPOSE) logs -f

.PHONY: ps
ps: ## Container-Status anzeigen
	@$(COMPOSE) ps

.PHONY: help
help: ## Diese Hilfe anzeigen
	@echo ""
	@echo "Verfügbare Befehle:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)make %-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# Standard-Target
.DEFAULT_GOAL := help
