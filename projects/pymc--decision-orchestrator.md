# Decision Orchestrator — PyMC Labs

Discord-based organizational OS for coordinating AI agents and workflows across teams.

## What It Does

1. Team member sends a message in Discord
2. Intelligent classifier analyzes intent
3. Workflow engine selects the appropriate database-driven workflow (scoped to server/channel)
4. Tool assembler dynamically provisions the right MCP tools
5. Claude Agent SDK executes with injected context and scoped credentials
6. Results flow back into Discord thread with full session persistence

This is agent infrastructure — a programmable orchestration layer where the LLM is the routing engine, not the product.

## Tech Stack

### Core
- Python 3.12+, discord.py
- Claude Agent SDK — AI orchestration layer
- Composio — 50+ external service integrations

### MCP Tool System (The Differentiator)
- Custom MCP tool registry — NOT FastMCP. Hand-built protocol implementation.
- `@tool` decorator — register functions as MCP tools with metadata
- Context injection — tools receive runtime context (user, channel, server, credentials)
- Scope-based credential gating — tools only access credentials they're authorized for, scoped per server/channel
- Dynamic tool assembly — each request gets a custom tool set based on workflow + context

### Database & Persistence
- Supabase (PostgreSQL)
- SQLAlchemy 2.0 — async ORM patterns
- Thread session persistence across Claude, Langfuse, and database layers

### Infrastructure
- FastAPI — webhook endpoints for external integrations
- Langfuse — LLM observability and tracing
- Fly.io — deployment

### Architecture
- FCIS (Functional Core, Imperative Shell) — pure functional logic at core, side effects pushed to edges

## Key Features Built

- Workflow-based orchestration — database-driven workflows scoped to Discord servers/channels, not hardcoded
- Intelligent message routing — classifier → workflow selection → tool assembly pipeline
- Custom MCP tool registry — protocol-level implementation with context injection and scope-based access control
- Thread session persistence — sessions span Claude context, Langfuse traces, and Supabase records; survive crashes and enable full audit trails
- Multi-platform integrations — Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io
- Discord archive sync — bulk sync of Discord history to Supabase Storage
- Shared client library — `orchestrator-clients` package for extensibility

## Scale

| Metric | Value |
|--------|-------|
| Python files | ~285 |
| LOC | ~36,400 |
| Direct dependencies | 24 |
| Database tables | 5+ |

## PyMC Labs Context

PyMC Labs is the professional services / product arm of the PyMC project (widely used probabilistic programming library). Decision Orchestrator is the internal infrastructure PyMC Labs uses to run its own operations — an AI-powered organizational OS trusted by people who build statistical modeling frameworks.

## Architectural DNA

Shares architectural patterns with [[nutsandbolts--cheerful]]:
- Claude Agent SDK as core orchestration layer
- MCP tool servers (built, not just consumed)
- Supabase (PostgreSQL)
- Langfuse observability
- Composio integrations

Different domains (organizational OS vs marketing automation), same platform thesis.

## Notes

