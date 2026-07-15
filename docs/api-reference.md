# 📡 API Reference

**Base URL:** `http://localhost:8000`

All endpoints return JSON. Dates use ISO 8601 format. UUIDs are used for all resource identifiers.

---

## Table of Contents

- [POST /chat](#post-chat)
- [POST /interaction](#post-interaction)
- [PUT /interaction/{id}](#put-interactionid)
- [GET /interaction/{id}](#get-interactionid)
- [GET /doctor/{name}](#get-doctorname)
- [GET /history](#get-history)
- [GET /health](#get-health)

---

## POST /chat

Send a natural language message to the AI assistant. The assistant will classify intent, extract entities, and either log an interaction or answer a query.

**URL:** `/chat`

**Method:** `POST`

**Request Body:**

```json
{
  "message": "Had a great meeting with Dr. Sharma at Apollo today. Discussed CardioGuard trial results. She wants to prescribe it for 5 new patients.",
  "session_id": "optional-session-uuid"
}
```

| Field       | Type   | Required | Description                                       |
| ----------- | ------ | -------- | ------------------------------------------------- |
| `message`   | string | Yes      | Natural language input from the user               |
| `session_id`| string | No       | Session ID for multi-turn conversation context     |

**Response (200 OK):**

```json
{
  "response": "I've logged your interaction with Dr. Priya Sharma at Apollo Hospital. Here's the summary...",
  "interaction": {
    "id": "d1b2c3d4-e5f6-7890-abcd-ef1234567801",
    "doctor": "Dr. Priya Sharma",
    "date": "2026-07-09",
    "type": "in-person",
    "sentiment": "positive",
    "summary": "Productive meeting discussing CardioGuard trial results...",
    "follow_up_actions": [
      "Send elderly subgroup data by Friday"
    ]
  },
  "intent": "log_interaction",
  "confidence": 0.95
}
```

**Error Responses:**

| Status | Description                                |
| ------ | ------------------------------------------ |
| 400    | Empty or invalid message                   |
| 422    | Validation error                           |
| 500    | AI pipeline or internal server error       |

---

## POST /interaction

Create a new interaction record directly (form-based / programmatic).

**URL:** `/interaction`

**Method:** `POST`

**Request Body:**

```json
{
  "hcp_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567801",
  "interaction_type": "in-person",
  "date": "2026-07-09",
  "time": "10:30:00",
  "attendees": ["Dr. Priya Sharma", "Anil Patil"],
  "topics_discussed": ["CardioGuard efficacy", "STELLAR trial"],
  "sentiment": "positive",
  "outcomes": "Dr. Sharma agreed to prescribe for 5 new patients.",
  "follow_up_actions": ["Send subgroup data by Friday"],
  "summary": "Productive meeting at Apollo Hospital..."
}
```

| Field              | Type     | Required | Description                                               |
| ------------------ | -------- | -------- | --------------------------------------------------------- |
| `hcp_id`           | UUID     | Yes      | ID of the healthcare professional                         |
| `interaction_type` | string   | Yes      | One of: `in-person`, `phone`, `email`, `video-call`, `conference` |
| `date`             | date     | Yes      | Date of the interaction (YYYY-MM-DD)                      |
| `time`             | time     | No       | Time of the interaction (HH:MM:SS)                        |
| `attendees`        | string[] | No       | List of people present                                    |
| `topics_discussed` | string[] | No       | Topics covered during the interaction                     |
| `sentiment`        | string   | No       | One of: `positive`, `neutral`, `negative`, `mixed`        |
| `outcomes`         | string   | No       | Key outcomes or decisions                                 |
| `follow_up_actions`| string[] | No       | List of follow-up items                                   |
| `summary`          | string   | No       | Text summary of the interaction                           |

**Response (201 Created):**

```json
{
  "id": "d1b2c3d4-e5f6-7890-abcd-ef1234567801",
  "message": "Interaction created successfully.",
  "created_at": "2026-07-09T10:30:00Z"
}
```

**Error Responses:**

| Status | Description                                |
| ------ | ------------------------------------------ |
| 400    | Invalid interaction type or missing fields |
| 404    | HCP with given ID not found                |
| 422    | Validation error                           |

---

## PUT /interaction/{id}

Update an existing interaction record.

**URL:** `/interaction/{id}`

**Method:** `PUT`

**Path Parameters:**

| Parameter | Type | Description                  |
| --------- | ---- | ---------------------------- |
| `id`      | UUID | The interaction's unique ID  |

**Request Body:**

Any subset of the fields from `POST /interaction`. Only provided fields will be updated.

```json
{
  "sentiment": "positive",
  "outcomes": "Updated outcomes after follow-up call.",
  "follow_up_actions": ["Schedule next meeting for August"]
}
```

**Response (200 OK):**

```json
{
  "id": "d1b2c3d4-e5f6-7890-abcd-ef1234567801",
  "message": "Interaction updated successfully.",
  "updated_at": "2026-07-09T15:00:00Z"
}
```

**Error Responses:**

| Status | Description                         |
| ------ | ----------------------------------- |
| 404    | Interaction not found               |
| 422    | Validation error                    |

---

## GET /interaction/{id}

Retrieve a single interaction by its ID, including related materials and samples.

**URL:** `/interaction/{id}`

**Method:** `GET`

**Path Parameters:**

| Parameter | Type | Description                  |
| --------- | ---- | ---------------------------- |
| `id`      | UUID | The interaction's unique ID  |

**Response (200 OK):**

```json
{
  "id": "d1b2c3d4-e5f6-7890-abcd-ef1234567801",
  "hcp": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567801",
    "name": "Dr. Priya Sharma",
    "hospital": "Apollo Hospital, Mumbai",
    "specialization": "Cardiology"
  },
  "interaction_type": "in-person",
  "date": "2026-07-01",
  "time": "10:30:00",
  "attendees": ["Dr. Priya Sharma", "Sales Rep: Anil Patil"],
  "topics_discussed": ["CardioGuard efficacy data", "STELLAR trial outcomes"],
  "sentiment": "positive",
  "outcomes": "Dr. Sharma agreed to trial CardioGuard for 5 new patients.",
  "follow_up_actions": ["Send elderly subgroup analysis by July 5"],
  "summary": "Productive meeting with Dr. Priya Sharma at Apollo Hospital...",
  "ai_generated": true,
  "materials": [
    { "id": "...", "name": "CardioGuard Product Brochure", "type": "brochure" }
  ],
  "samples": [
    { "id": "...", "name": "CardioGuard 10mg Starter Pack", "quantity": 5 }
  ],
  "created_at": "2026-07-01T10:30:00Z",
  "updated_at": "2026-07-01T10:30:00Z"
}
```

**Error Responses:**

| Status | Description            |
| ------ | ---------------------- |
| 404    | Interaction not found  |

---

## GET /doctor/{name}

Retrieve a doctor's profile and interaction history by name. Supports partial name matching.

**URL:** `/doctor/{name}`

**Method:** `GET`

**Path Parameters:**

| Parameter | Type   | Description                                      |
| --------- | ------ | ------------------------------------------------ |
| `name`    | string | Full or partial name of the doctor (URL-encoded) |

**Query Parameters:**

| Parameter | Type   | Default | Description                      |
| --------- | ------ | ------- | -------------------------------- |
| `limit`   | int    | 20      | Max number of interactions       |
| `offset`  | int    | 0       | Pagination offset                |

**Response (200 OK):**

```json
{
  "doctor": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567801",
    "name": "Dr. Priya Sharma",
    "hospital": "Apollo Hospital, Mumbai",
    "specialization": "Cardiology",
    "phone": "+91-9876543210",
    "email": "priya.sharma@apollo.com",
    "preferred_contact": "email",
    "notes": "Key opinion leader in interventional cardiology."
  },
  "interactions": [
    {
      "id": "d1b2c3d4-e5f6-7890-abcd-ef1234567801",
      "interaction_type": "in-person",
      "date": "2026-07-01",
      "sentiment": "positive",
      "summary": "Productive meeting discussing CardioGuard..."
    }
  ],
  "total_interactions": 1
}
```

**Error Responses:**

| Status | Description                           |
| ------ | ------------------------------------- |
| 404    | No doctor found matching the name     |

---

## GET /history

Retrieve a paginated list of all interactions with optional filters.

**URL:** `/history`

**Method:** `GET`

**Query Parameters:**

| Parameter          | Type   | Default | Description                                       |
| ------------------ | ------ | ------- | ------------------------------------------------- |
| `from_date`        | date   | —       | Filter interactions on or after this date          |
| `to_date`          | date   | —       | Filter interactions on or before this date         |
| `interaction_type` | string | —       | Filter by type (in-person, phone, email, etc.)     |
| `sentiment`        | string | —       | Filter by sentiment (positive, neutral, negative)  |
| `doctor`           | string | —       | Filter by doctor name (partial match)              |
| `limit`            | int    | 20      | Number of results per page (max 100)               |
| `offset`           | int    | 0       | Pagination offset                                  |
| `sort`             | string | `date`  | Sort field: `date`, `created_at`, `sentiment`      |
| `order`            | string | `desc`  | Sort order: `asc` or `desc`                        |

**Response (200 OK):**

```json
{
  "interactions": [
    {
      "id": "d1b2c3d4-e5f6-7890-abcd-ef1234567801",
      "doctor_name": "Dr. Priya Sharma",
      "interaction_type": "in-person",
      "date": "2026-07-01",
      "sentiment": "positive",
      "summary": "Productive meeting discussing CardioGuard...",
      "ai_generated": true
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

---

## GET /health

Health check endpoint for monitoring and load balancer probes.

**URL:** `/health`

**Method:** `GET`

**Response (200 OK):**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "ai_service": "available",
  "timestamp": "2026-07-09T12:00:00Z"
}
```

**Error Responses:**

| Status | Description                        |
| ------ | ---------------------------------- |
| 503    | Service unhealthy (DB or AI down)  |

---

## Common Error Response Format

All error responses follow a consistent format:

```json
{
  "detail": "A human-readable error message describing what went wrong.",
  "error_code": "RESOURCE_NOT_FOUND",
  "timestamp": "2026-07-09T12:00:00Z"
}
```

## Authentication

> **Note:** Authentication will be implemented in a future release. Currently, all endpoints are publicly accessible during development.

Planned authentication scheme:
- **Method:** JWT Bearer Token
- **Header:** `Authorization: Bearer <token>`
- **Token lifetime:** 24 hours
- **Refresh:** Via `/auth/refresh` endpoint
