# 🏥 AI-First CRM for HCP Interaction Management

An intelligent, AI-powered Customer Relationship Management system designed for pharmaceutical sales representatives to efficiently manage Healthcare Professional (HCP) interactions using conversational AI.

![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![React](https://img.shields.io/badge/react-19-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.115-teal.svg)
![LangGraph](https://img.shields.io/badge/langgraph-0.2-purple.svg)

## ✨ Key Features

### 🤖 AI-Powered Conversational Interface
- **Natural Language Interaction Logging** — Describe meetings in plain English, AI extracts structured CRM data
- **Intelligent Form Auto-Fill** — AI automatically populates interaction forms with extracted data
- **Follow-up Suggestions** — Context-aware action item recommendations
- **Meeting Summarization** — AI-generated professional meeting summaries

### 🧠 LangGraph Agentic Pipeline (5 Tools)
| Tool | Description |
|------|-------------|
| `log_interaction` | Extracts structured data from natural language descriptions |
| `edit_interaction` | Parses edit requests and updates specific CRM fields |
| `summarize_interaction` | Generates professional 2-paragraph meeting summaries |
| `suggest_followup` | Recommends contextual follow-up actions |
| `doctor_lookup` | Retrieves HCP profiles with interaction history |

### 📋 CRM Features
- Doctor/HCP profile management with search
- Interaction logging with sentiment tracking
- Material and sample distribution tracking
- Interaction history with filtering
- AI-generated vs manual interaction tracking

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────────────────────────┐
│   React 19 +    │     │          FastAPI Backend              │
│   Redux Toolkit │◄───►│                                       │
│   Vanilla CSS   │ API │  ┌─────────────────────────────────┐ │
│                 │     │  │      LangGraph Pipeline          │ │
│  ┌───────────┐  │     │  │  Intent → Tool → Response       │ │
│  │ Chat Panel│  │     │  │                                  │ │
│  │ Form      │  │     │  │  5 AI Tools (Groq LLM)          │ │
│  │ History   │  │     │  └─────────────────────────────────┘ │
│  └───────────┘  │     │  ┌──────────────────────────────────┐│
│                 │     │  │  SQLAlchemy + SQLite/PostgreSQL   ││
└─────────────────┘     │  └──────────────────────────────────┘│
                        └─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** >= 18.x
- **Python** >= 3.10
- **Groq API Key** (free at [console.groq.com](https://console.groq.com))

### 1. Clone & Setup Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure Environment

Edit `backend/.env`:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 3. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 4. Setup & Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. Open the App

Visit **http://localhost:5173** — the CRM interface will be ready!

## 📁 Project Structure

```
AI-First-CRM-HCP/
├── frontend/               # React 19 + Redux Toolkit
│   ├── src/
│   │   ├── components/     # UI Components (Header, ChatPanel, Form, etc.)
│   │   ├── redux/          # State management (4 slices)
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API communication layer
│   │   └── utils/          # Helpers, validators, constants
│   └── public/
│
├── backend/                # FastAPI + LangGraph
│   ├── app/
│   │   ├── api/            # REST API routes
│   │   ├── database/       # SQLAlchemy models, seed data
│   │   ├── graph/          # LangGraph workflow (state, nodes, router)
│   │   ├── models/         # ORM models (Doctor, Interaction, etc.)
│   │   ├── prompts/        # LLM prompt templates
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic layer
│   │   ├── tools/          # 5 LangGraph AI tools
│   │   └── utils/          # Logger, parser, validator, formatter
│   └── requirements.txt
│
└── docs/                   # Documentation
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Redux Toolkit, Vanilla CSS, Axios |
| Backend | FastAPI, Pydantic V2, Uvicorn |
| AI Engine | LangGraph, LangChain, Groq API (Gemma2/Llama3) |
| Database | SQLAlchemy 2.0, SQLite (dev) / PostgreSQL (prod) |
| State | Redux Toolkit with 4 slices |

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Send message to AI assistant |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/interaction` | Create interaction |
| GET | `/api/v1/interactions` | List interactions |
| GET | `/api/v1/doctors` | List all doctors |
| GET | `/api/v1/doctor/search/{q}` | Search doctors |
| GET | `/api/v1/history/{name}` | Doctor interaction history |

