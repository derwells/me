# Cheerful — Nuts and Bolts AI

Full-stack email automation platform for influencer marketing campaigns.

## What It Does

1. **Search creators** — waterfall enrichment pipeline crawls bios and websites to build creator profiles
2. **AI-draft personalized outreach** — Claude generates tailored emails per creator, not mail-merge templates
3. **Execute campaigns at scale** — Gmail OAuth integration handles multi-account sending, threading, and tracking

Three apps in one repo:
- **Backend API** — Python/FastAPI, the core campaign engine
- **Web App** — Next.js 16+ / React 19 frontend, campaign management UI with multi-step wizard
- **Context Engine** — Slack bot for team operations, built on Claude Agent SDK + MCP tool orchestration + Onyx RAG

## Tech Stack

### Backend
- Python, FastAPI
- Temporal.io — durable workflow orchestration (workflows survive crashes, handle retries, maintain state)
- Claude SDK + Agent SDK — AI orchestration for email personalization
- Gmail API — OAuth multi-account management, email threading
- Composio — integration framework (50+ external service connectors)
- Supabase — PostgreSQL database
- Langfuse — LLM observability and tracing

### Frontend
- Next.js 16+, React 19
- TanStack Query (server state), Zustand (client state)
- Tailwind + Radix/shadcn UI components

### Context Engine (Slack Bot)
- Slack Bolt
- Claude Agent SDK
- Onyx RAG — retrieval-augmented generation for team context
- MCP servers — tool orchestration for team operations

## Key Features Built

- Campaign management system — full CRUD + workflow for influencer outreach
- Creator search & enrichment — waterfall pipeline: multi-source bio crawling, website parsing, profile building
- AI-powered personalized email drafting — Claude generates individualized emails (not templates with variable insertion)
- Gmail OAuth integration — multi-account management, email threading and tracking
- Temporal-based durable workflows — campaign execution pipelines that survive failures and retry intelligently
- Slack Context Engine — team AI assistant with MCP tool orchestration
- Multi-step campaign wizard — frontend UX with email preview and review workflow before send

## Scale

| Metric | Value |
|--------|-------|
| Source files | ~2,170 |
| LOC | ~13,100 |
| Total commits | ~5,570 |
| Apps | 3 (backend, webapp, context-engine) |
| Team size | 5 |

## Architectural DNA

Shares architectural patterns with [[pymc--decision-orchestrator]]:
- Claude Agent SDK as core orchestration layer
- MCP tool servers (built, not just consumed)
- Supabase (PostgreSQL)
- Langfuse observability
- Composio integrations

Different domains (marketing automation vs organizational OS), same platform thesis.

## Notes

