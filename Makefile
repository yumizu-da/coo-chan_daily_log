.PHONY: format
format:
	uv run ruff format .
	uv run mdformat *.md

.PHONY: lint
lint:
	uv run ruff check .
	uv run mypy .
	uv run mdformat --check *.md

.PHONY: streamlit
streamlit:
	uv run --no-sync --env-file .env streamlit run app.py
