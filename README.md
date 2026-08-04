# Autonomous Enterprise Triage & Compliance Guard (AETCG)

AETCG is a modular security orchestration and compliance platform for ingesting enterprise event telemetry, protecting sensitive data, analyzing threats through asynchronous agents, and managing incidents with automated routing and human governance checkpoints.

## Overview

AETCG is built for security operations and compliance teams that require a scalable system to process high-volume corporate event traffic while preserving privacy, supporting policy-driven workflows, and maintaining an audit-ready incident trail.

## Key Features

* Secure ingestion and normalization of event payloads.
* Sensitive data scrubbing and de-identification before analysis.
* Asynchronous agent-based threat scoring and anomaly detection.
* Policy-driven workflow routing and incident lifecycle management.
* Human governance gates for approval, review, and escalation.
* Audit logging for traceability and compliance.
* Docker Compose deployment for local orchestration.

## Architecture

AETCG consists of several primary layers:

1. Ingestion
   * Accepts external event feeds and validates payloads.
   * Redacts sensitive fields and converts data into a canonical format.
2. Analysis
   * Executes isolated agents to score risk and detect compliance issues.
   * Uses asynchronous processing to scale across high volumes.
3. Routing
   * Applies workflow rules to determine the next incident state.
   * Automates state transitions while enforcing policy checks.
4. Governance
   * Enforces human review gates for high-risk actions.
   * Captures decision metadata for audit and reporting.

## Repository Structure

* `agent/` – analysis agents and scoring modules.
* `ingest/` – event intake, validation, and redaction logic.
* `routing/` – workflow engine and state transition rules.
* `governance/` – approval workflows and audit recording.
* `tests/` – validation, integration, and end-to-end tests.
* `docker-compose.yml` – local deployment manifest.
* `.env.example` – sample environment configuration.

## Prerequisites

* Docker Desktop installed and running locally.
* Python 3.11 for manual validation and test execution.
* `git` for repository cloning.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/example/aetcg-platform.git
   cd aetcg-platform
   ```

2. Create a local environment configuration:
   ```bash
   cp .env.example .env
   ```

3. Update `.env` with deployment-specific values such as service ports, queue/topic settings, database connections, and governance modes.

4. Launch the platform:
   ```bash
   docker compose up --build
   ```

5. Verify service startup via Docker logs and available health endpoints.

## Configuration

AETCG uses environment variables to configure runtime behavior. Common settings include:

* `SERVICE_PORT` – API or orchestrator listening port.
* `INGEST_TOPIC` – messaging queue or topic for incoming telemetry.
* `AGENT_TIMEOUT` – maximum processing time for analysis agents.
* `GOVERNANCE_MODE` – review policy mode (`auto`, `manual`, `hybrid`).

Edit `.env` to reflect your local or production environment settings.

## Local Development and Testing

1. Activate a Python 3.11 virtual environment.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run the test suite:
   ```bash
   python -m pytest tests/
   ```

## Troubleshooting

* If Docker Compose does not start, verify that required ports are available and environment variables are correct.
* If ingestion fails, confirm queue/topic names and connection settings.
* If agents time out, review the analysis logic and increase `AGENT_TIMEOUT` as needed.

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Add or update tests.
4. Open a pull request with a clear summary of your changes.

## License

See the `LICENSE` file in the repository for project licensing terms.
