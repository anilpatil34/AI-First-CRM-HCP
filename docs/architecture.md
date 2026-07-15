# 🏗️ Architecture Overview

## System Architecture

The AI-First Healthcare CRM follows a three-tier architecture with an embedded AI pipeline that processes natural language inputs into structured interaction records.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│                                                             │
│   React SPA (Single Page Application)                       │
│   ├── Chat Interface (primary interaction mode)             │
│   ├── Interaction History & Timeline                        │
│   ├── HCP Profile Cards                                     │
│   └── Dashboard & Analytics                                 │
│                                                             │
│   Communication: REST API via Axios                         │
│   State Management: React Context + useReducer              │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/JSON (Port 3000 → 8000)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                                                             │
│   FastAPI (Python 3.11+)                                    │
│   ├── API Router Layer (routes/)                            │
│   │   ├── /chat         → AI-powered conversation           │
│   │   ├── /interaction  → CRUD for interactions             │
│   │   ├── /doctor       → HCP profile management            │
│   │   └── /history      → Interaction history & search      │
│   │                                                         │
│   ├── Service Layer (services/)                             │
│   │   ├── ChatService       → Orchestrates AI pipeline      │
│   │   ├── InteractionService → Business logic               │
│   │   └── DoctorService     → HCP profile operations        │
│   │                                                         │
│   └── AI Pipeline (ai/)                                     │
│       └── LangGraph Workflow                                │
│           ├── Intent Classification Node                    │
│           ├── Entity Extraction Node                        │
│           ├── Sentiment Analysis Node                       │
│           └── Summary Generation Node                       │
│                                                             │
│   External: Groq API (LLaMA model inference)                │
└──────────────────────┬──────────────────────────────────────┘
                       │ SQL via asyncpg / SQLAlchemy
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│                                                             │
│   PostgreSQL 15+                                            │
│   ├── hcp_profiles          → Doctor information            │
│   ├── hcp_interactions      → Meeting/call/email records    │
│   ├── materials             → Marketing collateral          │
│   ├── samples               → Product sample inventory      │
│   ├── interaction_materials → Junction table                │
│   └── interaction_samples   → Junction table                │
│                                                             │
│   Features: UUID PKs, JSONB, Array columns, Triggers        │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Chat-Based Interaction Logging

This is the primary workflow — a sales rep describes a meeting in natural language, and the system extracts structured data automatically.

```
User types: "Had a great meeting with Dr. Sharma at Apollo today.
             Discussed CardioGuard trial results. She wants to
             prescribe it for 5 new patients. Need to send her
             the elderly subgroup data by Friday."

     │
     ▼
┌─────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  React UI   │────▶│  POST /chat      │────▶│  LangGraph        │
│  Chat Input │     │  FastAPI Route    │     │  Pipeline         │
└─────────────┘     └──────────────────┘     └───────┬───────────┘
                                                     │
                    ┌────────────────────────────────┘
                    ▼
        ┌───────────────────┐
        │  1. CLASSIFY       │  Determine intent:
        │     INTENT         │  → "log_interaction"
        └─────────┬─────────┘
                  ▼
        ┌───────────────────┐
        │  2. EXTRACT        │  Extract entities:
        │     ENTITIES       │  → doctor: "Dr. Sharma"
        │                    │  → hospital: "Apollo"
        │                    │  → topics: ["CardioGuard trial"]
        │                    │  → outcome: "prescribe 5 patients"
        │                    │  → follow-up: "send data by Friday"
        └─────────┬─────────┘
                  ▼
        ┌───────────────────┐
        │  3. ANALYZE        │  Determine sentiment:
        │     SENTIMENT      │  → "positive"
        └─────────┬─────────┘
                  ▼
        ┌───────────────────┐
        │  4. GENERATE       │  Create professional summary
        │     SUMMARY        │  and structured record
        └─────────┬─────────┘
                  ▼
        ┌───────────────────┐
        │  5. STORE &        │  Save to PostgreSQL
        │     RESPOND        │  Return confirmation + summary
        └───────────────────┘
```

### 2. Direct API Interaction

For programmatic access or form-based input, clients can use the REST API directly:

```
Client → POST /interaction (JSON body) → Validate → Store → Respond
Client → GET /doctor/{name}            → Query   → Format → Respond
Client → GET /history?from=...&to=...  → Query   → Paginate → Respond
```

---

## AI Pipeline (LangGraph)

The AI pipeline is built as a **LangGraph StateGraph** — a directed acyclic graph where each node performs a specific NLP task and passes state to the next node.

### Graph Nodes

| Node              | Input                   | Output                              | LLM Call |
| ----------------- | ----------------------- | ----------------------------------- | -------- |
| `classify_intent` | Raw user message        | Intent label + confidence           | Yes      |
| `extract_entities`| Message + intent        | Structured entities (doctor, date…) | Yes      |
| `analyze_sentiment`| Message + entities     | Sentiment label + reasoning         | Yes      |
| `generate_summary`| All extracted data      | Professional summary text           | Yes      |
| `store_record`    | Complete structured data| Database record ID                  | No       |

### State Schema

```python
class InteractionState(TypedDict):
    user_message: str
    intent: str
    entities: dict          # doctor, date, topics, outcomes, etc.
    sentiment: str          # positive | neutral | negative | mixed
    summary: str            # AI-generated professional summary
    interaction_id: str     # UUID of saved record
    response: str           # Message to return to the user
```

### Error Handling

- If entity extraction fails, the system asks clarifying questions
- If doctor name is ambiguous, it suggests matching profiles
- All LLM calls include retry logic with exponential backoff
- Groq API failures fall back to a basic extraction heuristic

---

## Component Interactions

### Frontend Components

```
App
├── ChatPage
│   ├── ChatWindow
│   │   ├── MessageList
│   │   │   ├── UserMessage
│   │   │   └── AIMessage (with structured data card)
│   │   └── ChatInput
│   └── InteractionPreview (side panel)
│
├── DashboardPage
│   ├── StatsCards (total interactions, doctors, sentiment breakdown)
│   ├── RecentInteractions
│   └── UpcomingFollowUps
│
├── DoctorPage
│   ├── DoctorProfile
│   ├── InteractionTimeline
│   └── MaterialsHistory
│
└── HistoryPage
    ├── FilterBar (date range, type, sentiment)
    └── InteractionTable
```

### Backend Module Structure

```
backend/
├── app/
│   ├── main.py              → FastAPI app initialization
│   ├── config.py            → Environment & settings
│   ├── models/              → Pydantic schemas & DB models
│   ├── routes/              → API endpoint handlers
│   ├── services/            → Business logic layer
│   ├── ai/                  → LangGraph pipeline
│   │   ├── graph.py         → StateGraph definition
│   │   ├── nodes.py         → Individual graph nodes
│   │   ├── prompts.py       → LLM prompt templates
│   │   └── state.py         → State type definitions
│   └── database/            → DB connection & queries
```

---

## Technology Decisions

| Decision                      | Rationale                                                         |
| ----------------------------- | ----------------------------------------------------------------- |
| **LangGraph** over LangChain  | Better control over multi-step AI workflows with explicit state   |
| **Groq** over OpenAI          | 10x faster inference for real-time chat; cost-effective           |
| **PostgreSQL** over MongoDB   | Structured CRM data benefits from relational integrity & joins    |
| **FastAPI** over Flask/Django  | Async support, auto-docs, Pydantic validation, high performance   |
| **React** over Next.js        | SPA is sufficient; no SSR needed for internal CRM tool            |
| **UUID** primary keys         | Avoid sequential ID enumeration; better for distributed systems   |

---

## Deployment Architecture (Production)

```
                    ┌──────────────┐
                    │   Nginx /    │
                    │  Cloud LB    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼                         ▼
     ┌────────────────┐       ┌────────────────┐
     │  React Static  │       │   FastAPI       │
     │  (CDN/S3)      │       │  (Gunicorn +    │
     │                │       │   Uvicorn)      │
     └────────────────┘       └───────┬────────┘
                                      │
                              ┌───────┴────────┐
                              ▼                ▼
                     ┌──────────────┐  ┌──────────────┐
                     │ PostgreSQL   │  │  Groq API    │
                     │ (RDS/Cloud)  │  │  (External)  │
                     └──────────────┘  └──────────────┘
```
