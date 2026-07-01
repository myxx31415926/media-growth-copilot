1. System Core Philosophy

Observe → Analyze → Predict → Recommend → Notify

This is the only allowed execution flow for all agents.

⸻

2. System Architecture

The system is Adapter-driven + Agent-based architecture

⸻

2.1 Data Collection Layer (UPDATED)

Responsible for ingesting external data via adapters.

Supported Adapters (MVP + Competition):

* CSVAdapter (development only)
* VOCAdapter (primary competition source)
* APIAdapter (company system)

Rules:

* Collector MUST NOT depend on data source type
* All external systems MUST be abstracted as adapters

⸻

2.2 Storage Layer (CLARIFIED)

MVP storage:

* SQLite (for local persistence and traceability)

Rules:

* All ingested data must be optionally persisted
* System MUST support working without database (mock mode allowed)
* No business logic inside storage layer

⸻

2.3 Intelligence Layer

Responsible for:

* Deterministic metric computation
* Rule-based prediction
* Insight interpretation

Key Metrics:

* engagement_rate
* like_ratio
* comment_ratio

Rules:

* No ML models in Sprint 1–3
* AI is used ONLY for interpretation, not calculation

⸻

2.4 Action Layer

Responsible for:

* Feishu notifications
* Comment intelligence
* Reporting output

Rules:

* Human-in-the-loop required
* All external actions must support dry-run mode
* No auto-posting allowed

⸻

3. Codex Execution Principle

“Implement exactly what is requested, nothing more.”