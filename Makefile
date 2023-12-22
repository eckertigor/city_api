#!/usr/bin/env make

.DEFAULT_GOAL: help

MAKEFLAGS=--no-print-directory

DOCKER_COMPOSE?=docker-compose

.PHONY: help
help: ## List all Python Makefile targets
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

##
## Python Containers
##
.PHONY: build
build: ## Build the python docker image
	docker build --label city-api --tag city-api .

.PHONY:
run:  ## Run a python-fastapi container
	$(DOCKER_COMPOSE) up
## $(DOCKER_COMPOSE) run -p 1337:1337 app python api/main.py

.PHONY: shell
shell: ## Open a bash shell on a python-fastapi container
	$(DOCKER_COMPOSE) run -p 1337:1337 app bash

##
## Python Tests
##
.PHONY: test
test: ## Shortcut to launch all the test tasks (unit, functional and integration).
		$(DOCKER_COMPOSE) run -p 1337:1337 app python -m pytest api/tests/ -v

.PHONY: clean
clean: ## Remove containers
	$(DOCKER_COMPOSE) down --remove-orphans

.PHONY: clean-all
clean-all:
	$(DOCKER_COMPOSE) down --remove-orphans -v
	docker image prune --filter label=city-api -af

.PHONY: all
all: build ## Build and test
