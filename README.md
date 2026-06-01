# Autonomous Enterprise Triage & Compliance Guard (AETCG)

AETCG is an advanced, multi-agent platform designed to securely ingest corporate event traffic, scrub sensitive details, analyze threat levels asynchronously, and execute automated state routing with built-in human governance gates.

## Core Infrastructure Quickstart

### Prerequisites
* Docker Desktop installed and running locally.
* Python 3.11 environment (if executing individual validation tests manually).

### Deployment Sequence
1. Clone the repository and initialize the environment profile parameters:
   ```bash
   cp .env.example .env