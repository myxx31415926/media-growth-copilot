📘 Media Growth Copilot

AI-powered Media Intelligence System for content performance analysis and growth optimization.

⸻

🎯 What it does

Transforms raw social media data (VOC / APIs / datasets) into actionable insights:

* Content performance analysis
* Viral content prediction
* Engagement metrics computation
* Comment classification
* Operational alerts

⸻

🧠 Core Concept

Observe → Analyze → Predict → Recommend → Notify

Powered by modular AI Agent architecture.

⸻

🧩 System Overview

The system is built on an Adapter-based architecture:

* CSVAdapter (development)
* VOCAdapter (competition primary source)
* APIAdapter (company system)

⸻

⚙️ Architecture Layers

* Data Collection Layer (Adapter-based ingestion)
* Storage Layer (SQLite optional persistence)
* Intelligence Layer (metrics + prediction)
* Action Layer (Feishu + insights output)

⸻

🚀 Key Features

* Multi-source data ingestion (VOC / API / CSV)
* Rule-based engagement analysis
* Viral content scoring system
* Comment classification system
* Human-in-the-loop action system

⸻

🏁 Current Status

Sprint 1: Data ingestion pipeline (in progress)

⸻

📌 Design Principles

* Deterministic logic first
* No ML in early sprints
* Modular Agent architecture
* External systems abstracted as Adapters
* Fail-safe dry-run for all actions