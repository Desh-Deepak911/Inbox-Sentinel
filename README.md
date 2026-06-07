# Inbox Sentinel

**Inbox Sentinel** is a local-first AI email assistant that helps users identify important emails, prioritize their inbox, and receive actionable insights without surrendering control of their data.

The project is being built incrementally to demonstrate how modern AI agents can be designed using real-world software engineering principles such as authentication, state management, rule engines, memory, notifications, and AI-powered reasoning.

## Vision

Most people don't need another inbox.

They need a system that answers:

- Which emails require my attention?
- What should I respond to first?
- What can safely wait?
- What actions are required from me?

Inbox Sentinel aims to become a personal email chief of staff that runs locally and helps users focus on what matters.

## Current Features

### Gmail Authentication

- OAuth 2.0 integration with Gmail API
- Secure token-based authentication
- Read-only Gmail access

### Email Retrieval

- Fetch unread inbox emails
- Extract sender information
- Extract email subject
- Extract email snippet
- Extract email metadata

### Rule-Based Priority Engine

- Keyword-based urgency detection
- Sender importance scoring
- Priority classification:
  - HIGH
  - MEDIUM
  - LOW
- Explainable reasoning for every classification

### Local Memory

- SQLite-based persistence
- Stores processed email information
- Prevents duplicate processing
- Maintains state across executions

## Architecture

```text
Gmail API
    ↓
OAuth Authentication
    ↓
Email Retrieval
    ↓
Rule Engine
    ↓
SQLite Memory
    ↓
User Output
```

## Tech Stack

- Python
- Gmail API
- OAuth 2.0
- SQLite
- Google API Client Library

## Project Structure

```text
inbox-sentinel/
├── src/
│   ├── main.py
│   ├── gmail_client.py
│   ├── rules.py
│   └── db.py
│
├── tests/
├── docs/
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

## Roadmap

### Phase 1
- [x] Gmail OAuth Authentication
- [x] Read Unread Emails

### Phase 2
- [x] Rule-Based Priority Scoring
- [x] SQLite Memory Layer

### Phase 3
- [ ] Desktop Notifications
- [ ] Priority-Based Alerts

### Phase 4
- [ ] AI Email Classification
- [ ] Action Extraction
- [ ] Deadline Detection

### Phase 5
- [ ] Daily Inbox Digest
- [ ] Reminder Scheduling
- [ ] Follow-Up Detection

### Phase 6
- [ ] Plugin Architecture
- [ ] Custom User Rules
- [ ] Multi-Provider Email Support

## Security

Inbox Sentinel is designed with a privacy-first philosophy.

Never commit:

- credentials.json
- token.json
- .env files

All Gmail credentials remain local to the user's machine.

## Why This Project Exists

This project serves two purposes:

1. Build a genuinely useful personal productivity tool.
2. Learn and demonstrate how production-grade AI agents are architected beyond simple LLM prompts.

The goal is to show how authentication, memory, reasoning, persistence, and action systems come together to form intelligent software.