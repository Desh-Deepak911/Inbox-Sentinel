# Inbox Sentinel

Inbox Sentinel is an open-source, local-first AI email assistant that helps users identify important emails, remember pending actions, generate reminders, and provide actionable insights from their inbox.

The goal is not to build another inbox client, but to build an intelligent email assistant that helps users decide:

- What needs my attention?
- What should I do next?
- What can wait?
- What have I forgotten to follow up on?

## Vision

Inbox Sentinel aims to become a personal email chief of staff that:

- Watches incoming emails
- Prioritizes important conversations
- Remembers pending actions
- Reminds users when action is needed
- Drafts intelligent responses
- Maintains user control and privacy

All processing is performed locally, with user-controlled AI integrations.

---

# Current Features

## Gmail Authentication

- OAuth 2.0 Gmail authentication
- Secure token-based access
- Gmail API integration

## Email Retrieval

- Fetch unread emails
- Extract metadata
- Extract sender information
- Extract subjects and snippets

## Rule-Based Classification

- Keyword scoring
- Important sender detection
- Explainable classifications
- Priority levels:
  - HIGH
  - MEDIUM
  - LOW

## AI Classification

Powered by Gemini.

Provides:

- Priority assessment
- Reasoning
- Suggested actions
- Confidence scoring

Example:

```json
{
  "priority": "HIGH",
  "reason": "Recruiter is requesting interview availability.",
  "suggested_action": "Reply with available interview slots.",
  "confidence": 0.92
}
```

## Local Memory

SQLite persistence for:

- Processed emails
- AI insights
- Suggested actions
- Confidence scores

## Daily Digest

Generate summaries of:

- High-priority emails
- Medium-priority emails
- Recommended actions

## Notifications

Desktop notifications for priority emails.

## Scheduled Monitoring

Inbox Sentinel can:

- Monitor Gmail periodically
- Classify emails automatically
- Update memory continuously

## Reminder Agent

ReminderAgent determines:

- Whether an email requires a reminder
- When reminders should occur
- Reminder priority

## Reminder Persistence

Reminders are stored in SQLite and survive restarts.

## Due Reminder Processing

Inbox Sentinel can:

- Find due reminders
- Send reminder notifications
- Mark reminders as completed

---

# Architecture

```text
Gmail API
    ↓
Email Fetcher
    ↓
Rule Classifier
    ↓
AI Classifier (Gemini)
    ↓
Memory Store (SQLite)
    ↓
Reminder Agent
    ↓
Reminder Store
    ↓
Notification Adapter
```

## Scheduled Agent Loop

```text
Observe Inbox
    ↓
Classify
    ↓
Generate AI Insights
    ↓
Store Email Memory
    ↓
Create Reminder
    ↓
Store Reminder
    ↓
Send Notifications
    ↓
Check Due Reminders
    ↓
Repeat
```

---

# Project Structure

```text
src/
└── inbox_sentinel/
    ├── __init__.py
    ├── main.py
    │
    ├── ai/
    │   └── email_classifier.py
    │
    ├── classifiers/
    │   └── rule_classifier.py
    │
    ├── config/
    │   └── loader.py
    │
    ├── digest/
    │   └── generator.py
    │
    ├── gmail/
    │   └── client.py
    │
    ├── memory/
    │   └── sqlite_store.py
    │
    ├── notifications/
    │   └── notifier.py
    │
    └── reminders/
        └── reminder_agent.py
```

---

# Technology Stack

- Python
- Gmail API
- OAuth 2.0
- SQLite
- APScheduler
- Gemini API
- PyYAML

---

# Current Roadmap

## Completed

- [x] Gmail OAuth Authentication
- [x] Email Retrieval
- [x] Rule-Based Classification
- [x] Gemini AI Classification
- [x] SQLite Memory Layer
- [x] Daily Digest Generation
- [x] Desktop Notifications
- [x] Scheduled Inbox Monitoring
- [x] Project Structure Refactor
- [x] ReminderAgent
- [x] Reminder Persistence
- [x] Due Reminder Processing

---

## In Progress

- [ ] Improve Notification Adapters

---

## Upcoming

### Memory Management

- [ ] Database cleanup policies
- [ ] Retention rules by priority
- [ ] Reminder lifecycle management

### Email Actions

- [ ] Reply Draft Agent
- [ ] Reply intent detection
- [ ] AI-generated response drafts
- [ ] Gmail draft creation
- [ ] User approval workflow
- [ ] Draft history

### User Experience

- [ ] CLI commands
- [ ] Reminder management commands
- [ ] Digest generation commands
- [ ] Interactive review workflow

### Reliability

- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end workflow tests
- [ ] CI/CD pipeline

### Documentation

- [ ] Architecture diagrams
- [ ] Development guide
- [ ] Contribution guide
- [ ] Deployment guide

---

# Long-Term Vision

Inbox Sentinel is evolving from an email classifier into an intelligent email assistant.

Future capabilities include:

- Intelligent reminders
- Follow-up tracking
- AI-generated drafts
- Email action recommendations
- Multi-channel notifications
- Multi-provider email support
- Personal workflow automation

The long-term objective is to create an open-source, privacy-first email assistant that helps users stay on top of important communications without surrendering control of their inbox.

---

# Security

Never commit:

- credentials.json
- token.json
- .env
- SQLite databases

All credentials remain local to the user's machine.

---

# Philosophy

Inbox Sentinel follows a simple principle:

> AI may recommend.
> AI may draft.
> AI may remind.
> The user remains in control.
