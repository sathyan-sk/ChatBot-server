# AI Knowledge Platform - Backend
Application-scoped, multi-tenant RAG backend. FastAPI (stateless API) + separate worker
process (ingestion + conversation cleanup). PostgreSQL + pgvector via Supabase.

## Prerequisites
- Python 3.12+
- Docker Desktop (for containerized run; DB itself is remote Supabase, not local)
- A Supabase project with the `vector` extension enabled on its Postgres database

## Setup (Windows / PowerShell)

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install uv
    uv pip install -e ".[dev]"
    Copy-Item .env.example .env
    alembic upgrade head
    uvicorn app.main:app --reload
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
Run the worker in a separate terminal:

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
Step 1 —
Open a new PowerShell terminal in VS Code.

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

Step 4 — Remove a broken virtual environment if necessary

If .venv already exists and you've experienced environment/path problems, cleanly recreate it.

First deactivate if currently activated:

deactivate

Then:

Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

This is safe because .venv contains generated environment files, not your application source.


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

## Project Structure
finalized application structure:
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── admin/
│   │   │   ├── admin_auth.py
│   │   │   ├── applications.py
│   │   │   ├── application_credentials.py
│   │   │   ├── knowledge_base.py
│   │   │   ├── data_sources.py
│   │   │   ├── ingestion.py
│   │   │   ├── application_settings.py
│   │   │   ├── widget_configuration.py
│   │   │   └── conversations.py
│   │   ├── client/
│   │   │   └── client_conversations.py
│   │   ├── widget/
│   │   │   ├── widget_conversation.py
│   │   │   └── widget_config.py
│   │   └── system/
│   │       ├── health.py
│   │       └── diagnostics.py
│   └── dependencies/
│       ├── auth_admin.py
│       ├── auth_application.py
│       ├── auth_widget.py
│       └── database.py
│
├── worker/
│   ├── main.py
│   ├── jobs/
│   │   ├── ingestion_job.py
│   │   └── conversation_cleanup_job.py
│   ├── job_claimer.py
│   └── runner.py
│
├── schemas/
│   ├── admin_auth.py
│   ├── application.py
│   ├── knowledge_base.py
│   ├── data_source.py
│   ├── ingestion.py
│   ├── application_settings.py
│   ├── widget_configuration.py
│   ├── conversation.py
│   ├── chat_message.py
│   └── widget.py
│
├── services/
│   ├── admin_auth_service.py
│   ├── application_service.py
│   ├── data_source_service.py
│   ├── ingestion_service.py
│   ├── conversation_service.py
│   ├── chat_service.py
│   ├── application_settings_service.py
│   ├── widget_configuration_service.py
│   └── widget_access_service.py
│
├── domain/
│   ├── entities/
│   │   ├── application.py
│   │   ├── application_credential.py
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
│   │   ├── application_repository.py
│   │   ├── application_credential_repository.py
│   │   ├── knowledge_base_repository.py
│   │   ├── data_source_repository.py
│   │   ├── ingestion_job_repository.py
│   │   ├── document_chunk_repository.py
│   │   ├── application_settings_repository.py
│   │   ├── widget_configuration_repository.py
│   │   ├── conversation_repository.py
│   │   ├── chat_message_repository.py
│   │   └── message_citation_repository.py
│   └── provider_interfaces/
│       ├── llm_provider.py
│       ├── embedding_provider.py
│       ├── reranker_provider.py
│       ├── parser_provider.py
│       ├── storage_provider.py
│       └── vector_search_provider.py
│
├── rag_engine/
│   ├── pipelines/
│   │   ├── ingestion_pipeline.py
│   │   └── retrieval_pipeline.py
│   ├── ingestion/
│   │   ├── source_loaders/
│   │   │   ├── file_loader.py
│   │   │   ├── website_loader.py
│   │   │   └── csv_loader.py
│   │   ├── parsers/
│   │   │   ├── document_parser.py
│   │   │   ├── html_parser.py
│   │   │   ├── structured_parser.py
│   │   │   └── plain_text_parser.py
│   │   ├── normalizer.py
│   │   ├── chunker.py
│   │   ├── metadata_enricher.py
│   │   ├── embedding_generator.py
│   │   └── vector_indexer.py
│   ├── retrieval/
│   │   ├── query_embedder.py
│   │   ├── semantic_retriever.py
│   │   ├── keyword_retriever.py
│   │   ├── metadata_filter.py
│   │   ├── fusion.py
│   │   └── reranker.py
│   └── generation/
│       ├── prompt_builder.py
│       ├── evidence_evaluator.py
│       ├── generator.py
│       ├── citation_builder.py
│       └── response_formatter.py
│
├── infrastructure/
│   ├── database/
│   │   ├── connection.py
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   ├── application_model.py
│   │   │   ├── application_credential_model.py
│   │   │   ├── knowledge_base_model.py
│   │   │   ├── data_source_model.py
│   │   │   ├── ingestion_job_model.py
│   │   │   ├── document_chunk_model.py
│   │   │   ├── application_settings_model.py
│   │   │   ├── widget_configuration_model.py
│   │   │   ├── conversation_model.py
│   │   │   ├── chat_message_model.py
│   │   │   └── message_citation_model.py
│   │   └── repositories/
│   │       ├── application_repository_impl.py
│   │       ├── application_credential_repository_impl.py
│   │       ├── knowledge_base_repository_impl.py
│   │       ├── data_source_repository_impl.py
│   │       ├── ingestion_job_repository_impl.py
│   │       ├── document_chunk_repository_impl.py
│   │       ├── application_settings_repository_impl.py
│   │       ├── widget_configuration_repository_impl.py
│   │       ├── conversation_repository_impl.py
│   │       ├── chat_message_repository_impl.py
│   │       └── message_citation_repository_impl.py
│   └── providers/
│       ├── llm/
│       │   ├── openrouter_provider.py
│       │   ├── openai_provider.py
│       │   ├── gemini_provider.py
│       │   ├── ollama_provider.py
│       │   └── llm_provider_factory.py
│       ├── embeddings/
│       │   ├── nomic_provider.py
│       │   ├── openai_provider.py
│       │   ├── ollama_provider.py
│       │   └── embedding_provider_factory.py
│       ├── reranking/
│       │   ├── cross_encoder_provider.py
│       │   ├── cohere_provider.py
│       │   └── reranker_provider_factory.py
│       ├── parsing/
│       │   ├── docling_provider.py
│       │   ├── plain_text_provider.py
│       │   └── parser_provider_factory.py
│       ├── storage/
│       │   ├── supabase_storage_provider.py
│       │   ├── s3_storage_provider.py
│       │   └── storage_provider_factory.py
│       └── vector/
│           ├── pgvector_provider.py
│           └── vector_search_provider_factory.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── security_gateway.py
│   ├── rate_limiter.py
│   ├── logging.py
│   ├── provider_resolver.py
│   └── composition.py
│
├── exceptions/
│   ├── domain_exceptions.py
│   └── handlers.py
│
├── tests/
│   ├── unit/
│   └── integration/
├── migrations/
│   └── versions/
├── .env.example
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
