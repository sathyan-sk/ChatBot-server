# AI Knowledge Platform - Backend
Application-scoped, multi-tenant RAG backend. FastAPI (stateless API) + separate worker
process (ingestion + conversation cleanup). PostgreSQL + pgvector via Supabase.

## Prerequisites
- Python 3.12+,FastAPI,Uvicorn,SQLAlchemy,Alembic,Pydantic,pydantic-settings,psycopg,httpx,pytest,mypy

## Creation (Windows / PowerShell)
1. uv --version

2. Create the Python environment

uv venv --python 3.12

3. activate
.\.venv\Scripts\Activate.ps1

(verifiy)
python --version
python -c "import sys; print(sys.executable)"

4. Define dependencies in pyproject.toml
5. Phase 4 — Sync the environment
uv lock
uv sync

6. cp .env.example .env

7. Alembic (referr migration guide)

8. Running the APP....
python -m uvicorn app.main:app --reload  (or) uvicorn app.main:app --reload

9. clear cache of pychace
Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force; Get-ChildItem -Path . -File -Recurse -Include "*.pyc","*.pyo" | Remove-Item -Force

--------------------
# hint(
Traditional project
───────────────────
.venv
  └── pip
       └── requirements.txt


This- project
────────────
.venv
  └── managed by uv
       ├── pyproject.toml
       └── uv.lock
)

-----------------------------
Running the Worker in a (separate terminal):

    python -m worker.main

## Run with Docker Compose (api + worker only, DB remains remote Supabase)

    docker compose up --build
---------------------------------------------------------

## dev environment----
1. Initial setup
uv venv --python 3.12

2. Activate:

.\.venv\Scripts\Activate.ps1

3. Install/synchronize project dependencies:

uv sync

4. Development dependencies:

uv sync --extra dev

5. Run the application:

python -m uvicorn app.main:app --reload

Or through uv:

uv run uvicorn app.main:app --reload

# Boot the App for Run:
1. Run the application:

uv run uvicorn app.main:app

2. Or, if your .venv is activated:

python -m uvicorn app.main:app

3. uv run uvicorn app.main:app --reload
--------------------------------------------

# For password hashing:
python -c "import bcrypt; print(bcrypt.hashpw(b'YourStrongPasswordHere', bcrypt.gensalt()).decode())"

# Generate API_KEY_HASH_SALT:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET:
python -c "import secrets; print(secrets.token_urlsafe(64))"


---------
# Steps to be setuped this projetc created
Remove a broken virtual environment if necessary
If .venv already exists and you've experienced environment/path problems, cleanly recreate it.
First deactivate if currently activated:

deactivate
Then:

Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

This is safe because .venv contains generated environment files, not your application source.

step 1: Install uv

irm https://astral.sh/uv/install.ps1 | iex

Check Python:
python --version

Expected:
Python 3.12.x

Check uv:
uv --version

Expected something like:
uv 0.12.6
If uv is not recognized

Since you previously had this Windows PATH issue, first run:

$env:Path += ";$env:USERPROFILE\.local\bin"

Then:

uv --version

If it still fails, verify the executable:

Test-Path "$env:USERPROFILE\.local\bin\uv.exe"

If this returns:

True

run:

& "$env:USERPROFILE\.local\bin\uv.exe" --version

Then permanently add it to the user PATH if necessary:

[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:USERPROFILE\.local\bin",
    "User"
)

Close and reopen VS Code/PowerShell afterward.

Do not continue until:

uv --version

works normally.

Step 2 — Open the backend root

Your terminal should be inside:
D:\new_AI-Projects\chatbot\backend

Verify:
Get-Location

You should also see:
pyproject.toml

Check:
Test-Path .\pyproject.toml

Expected:
True

step 3
Verify pyproject.toml

Your dependency source of truth is:

backend/
└── pyproject.toml

Step 4 — 

Step 5 — Create the Python virtual environment

Use the project's required Python version:

uv venv --python 3.12

Expected:
Using CPython 3.12.x interpreter
Creating virtual environment at: .venv
Step 6 — Activate the environment
.\.venv\Scripts\Activate.ps1

Your prompt should become something similar to:
(backend) PS D:\new_AI-Projects\chatbot\backend>

Verify:
python --version

and:
python -c "import sys; print(sys.executable)"
Step 7 — Synchronize dependencies

Now run:
uv sync

If your pyproject.toml contains a development dependency group/extra configured as dev, use the project's configured form, for example:

uv sync --extra dev

The exact command depends on how the pyproject.toml was defined.

The result should create/update:

backend/
├── .venv/
├── pyproject.toml
└── uv.lock
What happens here?

uv:

reads pyproject.toml
       ↓
resolves dependencies
       ↓
creates/updates uv.lock
       ↓
installs dependencies into .venv

You should commit uv.lock to Git.

step 8:
Configure environment variables

Create:

.env

from:

.env.example

For example:

Copy-Item .env.example .env

Then configure your actual development values.
------
| Task                    | Command                                       |
| ----------------------- | --------------------------------------------- |
| Install uv              | `irm https://astral.sh/uv/install.ps1 \| iex` |
| Create venv             | `uv venv --python 3.12`                       |
| Add package             | `uv add package`                              |
| Add dev package         | `uv add --dev package`                        |
| Install/sync everything | `uv sync`                                     |
| Update lock             | `uv lock`                                     |
| Run Python              | `python ...`                                  |
| Run FastAPI             | `python -m uvicorn app.main:app --reload`     |

## Project Structure
app/            HTTP layer: routes + FastAPI dependencies
core/           Config, security, logging, composition root, rate limiting
domain/         Entities, repository interfaces, provider interfaces
infrastructure/ Database models/repositories, concrete AI/storage providers
rag_engine/     Ingestion and retrieval pipelines (framework-independent)
services/       Application use cases (business logic orchestration)
schemas/        Pydantic API request/response DTOs
worker/         Background job runner (ingestion, conversation cleanup)
exceptions/     Typed exception hierarchy + FastAPI handlers
migrations/     Alembic migrations
tests/          Unit and integration tests

finalized application structure:
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   ├── admin_auth.py
│   │   │   ├── applications.py
│   │   │   ├── application_api.py
│   │   │   ├── knowledge_base.py
│   │   │   ├── document.py
│   │   │   ├── ingestion.py
│   │   │   ├── application_settings.py
│   │   │   ├── widget_configuration.py
│   │   │   └── conversations.py
│   │   ├── client/
│   │   │   ├── __init__.py
│   │   │   └── client_conversations.py
│   │   ├── widget/
│   │   │   ├── __init__.py
│   │   │   ├── widget_conversation.py
│   │   │   └── widget_config.py
│   │   └── system/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       └── diagnostics.py
│   └── dependencies/
│       ├── __init__.py
│       ├── auth_admin.py
│       ├── auth_application.py
│       ├── auth_widget.py
│       └── database.py
│
├── worker/
│   ├── __init__.py
│   ├── main.py
│   ├── job_claimer.py
│   ├── runner.py
│   └── jobs/
│       ├── __init__.py
│       ├── ingestion_job.py
│       └── conversation_cleanup_job.py
│
├── schemas/
│   ├── __init__.py
│   ├── admin_auth.py
│   ├── application.py
│   ├── knowledge_base.py
│   ├── documents.py
│   ├── ingestion.py
│   ├── application_settings.py
│   ├── widget_configuration.py
│   ├── conversation.py
│   ├── chat_message.py
│   └── widget.py
│
├── services/
│   ├── __init__.py
│   ├── admin_auth_service.py
│   ├── application_service.py
│   ├── application_api_service.py
│   ├── knowledge_base_service.py
│   ├── document_service.py
│   ├── ingestion_service.py
│   ├── application_settings_service.py
│   ├── widget_configuration_service.py
│   ├── conversation_service.py
│   └── chat_service.py
│
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── application.py
│   │   ├── application_api.py
│   │   ├── knowledge_base.py
│   │   ├── data_source.py
│   │   ├── ingestion_job.py
│   │   ├── document_chunk.py
│   │   ├── application_settings.py
│   │   ├── widget_configuration.py
│   │   ├── conversation.py
│   │   ├── chat_message.py
│   │   └── message_citation.py
│   ├── repository_interfaces/
│   │   ├── __init__.py
│   │   ├── application_repository.py
│   │   ├── application_api_repository.py
│   │   ├── knowledge_base_repository.py
│   │   ├── document_repository.py
│   │   ├── ingestion_job_repository.py
│   │   ├── document_chunk_repository.py
│   │   ├── application_settings_repository.py
│   │   ├── widget_configuration_repository.py
│   │   ├── conversation_repository.py
│   │   ├── chat_message_repository.py
│   │   └── message_citation_repository.py
│   └── provider_interfaces/
│       ├── __init__.py
│       ├── llm_provider.py
│       ├── embedding_provider.py
│       ├── reranker_provider.py
│       ├── parser_provider.py
│       ├── storage_provider.py
│       └── vector_search_provider.py
│
├── rag_engine/
│   ├── __init__.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── ingestion_pipeline.py
│   │   └── retrieval_pipeline.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── normalizer.py
│   │   ├── chunker.py
│   │   ├── metadata_enricher.py
│   │   ├── embedding_generator.py
│   │   ├── vector_indexer.py
│   │   ├── source_loaders/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_loader.py
│   │   │   ├── website_loader.py
│   │   │   └── csv_loader.py
│   │   └── parsers/
│   │       ├── __init__.py
│   │       ├── document_parser.py
│   │       ├── html_parser.py
│   │       ├── structured_parser.py
│   │       └── plain_text_parser.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── query_embedder.py
│   │   ├── semantic_retriever.py
│   │   ├── keyword_retriever.py
│   │   ├── metadata_filter.py
│   │   ├── fusion.py
│   │   └── reranker.py
│   └── generation/
│       ├── __init__.py
│       ├── prompt_builder.py
│       ├── evidence_evaluator.py
│       ├── response_generator.py
│       ├── citation_builder.py
│       └── response_formatter.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── application_model.py
│   │   │   ├── application_api_model.py
│   │   │   ├── knowledge_base_model.py
│   │   │   ├── document_model.py
│   │   │   ├── ingestion_job_model.py
│   │   │   ├── document_chunk_model.py
│   │   │   ├── application_settings_model.py
│   │   │   ├── widget_configuration_model.py
│   │   │   ├── conversation_model.py
│   │   │   ├── chat_message_model.py
│   │   │   └── message_citation_model.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── application_repository_impl.py
│   │       ├── application_api_repository_impl.py
│   │       ├── knowledge_base_repository_impl.py
│   │       ├── document_repository_impl.py
│   │       ├── ingestion_job_repository_impl.py
│   │       ├── document_chunk_repository_impl.py
│   │       ├── application_settings_repository_impl.py
│   │       ├── widget_configuration_repository_impl.py
│   │       ├── conversation_repository_impl.py
│   │       ├── chat_message_repository_impl.py
│   │       └── message_citation_repository_impl.py
│   └── providers/
│       ├── __init__.py
│       ├── llm/
│       │   ├── __init__.py
│       │   ├── openrouter_provider.py
│       │   ├── openai_provider.py
│       │   ├── huggingface_provider.py
│       │   ├── ollama_provider.py
│       │   └── llm_provider_factory.py
│       ├── embeddings/
│       │   ├── __init__.py
│       │   ├── openai_provider.py
│       │   ├── ollama_provider.py
│       │   └── embedding_provider_factory.py
│       ├── reranking/
│       │   ├── __init__.py
│       │   ├── cross_encoder_provider.py
│       │   ├── cohere_provider.py
│       │   └── reranker_provider_factory.py
│       ├── parsing/
│       │   ├── __init__.py
│       │   ├── docling_provider.py
│       │   ├── plain_text_provider.py
│       │   └── parser_provider_factory.py
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── supabase_storage_provider.py
│       │   ├── s3_storage_provider.py
│       │   └── storage_provider_factory.py
│       └── vector/
│           ├── __init__.py
│           ├── pgvector_provider.py
│           └── vector_search_provider_factory.py
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── security.py
│   ├── security_gateway.py
│   ├── rate_limiter.py
│   ├── logging.py
│   ├── provider_resolver.py
│   └── composition.py
│
├── exceptions/
│   ├── __init__.py
│   ├── domain_exceptions.py
│   └── handlers.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   ├── integration/
│   │   └── __init__.py
│   └── conftest.py
│
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── Dockerfile
└── README.md
