# Project Settings
PYTHON = .venv/bin/python
UV = uv

.PHONY: help init install sync render lint format typecheck test check clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

init: ## Initialize the full project structure
	@mkdir -p src/common src/ann src/cnn src/rnn src/transformers src/gans assets/images
	$(UV) venv --python 3.12
	$(UV) sync
	@echo "Project initialized. Use 'make render SCENE=path/to/script.py:ClassName' to build."

sync: ## Sync environment with pyproject.toml
	$(UV) sync

render: ## Render a manim scene (usage: make render SCENE=path/to/script.py:SceneName)
	@if [ -z "$(SCENE)" ]; then \
		echo "Usage: make render SCENE=path/to/script.py:ClassName"; \
	else \
		$(PYTHON) -m manim -pqh $(SCENE); \
	fi

lint: ## Lint with ruff (check only, no changes)
	$(UV) run ruff check .

format: ## Auto-format and fix lint issues with ruff
	$(UV) run ruff format .
	$(UV) run ruff check --fix .

typecheck: ## Static type-check with mypy
	$(UV) run mypy src

test: ## Run the test suite with pytest
	$(UV) run pytest

check: lint typecheck test ## Run lint, type-check, and tests

clean: ## Remove virtual environment and cached media
	rm -rf .venv media __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

.DEFAULT_GOAL := help