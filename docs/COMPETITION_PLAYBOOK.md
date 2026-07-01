# 📘 COMPETITION_PLAYBOOK — Media Growth Copilot

## 1. Competition Objective

Transform raw VOC / Company API social media data into actionable growth intelligence using an AI Agent system.

The goal is not feature completeness, but:

> Demonstrate an end-to-end data → intelligence → insight → UI pipeline.

---

## 2. Winning Principle

Winning systems are those that:

- Connect existing company data (VOC)
- Use AI only for interpretation
- Produce clear business insights
- Show a stable end-to-end pipeline
- Demonstrate Agent-based architecture

---

## 3. System Architecture (Target)

VOC / Company API / Adapters
        ↓
Collector Agent (Normalization only)
        ↓
Analyzer Agent (Metrics)
        ↓
Predictor Agent (Scoring)
        ↓
Comment Agent (Classification)
        ↓
Flutter UI (Visualization)

---

## 4. Core Design Rules

### 4.1 Everything External is an Adapter

- VOCAdapter (primary in competition)
- APIAdapter (company AI/data)
- CSVAdapter (development only)

Collector must NOT depend on source type.

---

### 4.2 Deterministic First

- No ML models in Sprint 1–3
- All metrics must be rule-based
- AI is used only for interpretation

---

### 4.3 Agent Isolation

Each agent must be:

- Independent
- Stateless (as much as possible)
- Non-coupled

---

## 5. Sprint Strategy

### Sprint 1 — Data Foundation

- Adapter layer
- Collector
- Basic pipeline execution

### Sprint 2 — Intelligence Layer

- Analyzer Agent
- Engagement metrics
- Ranking

### Sprint 3 — Prediction Layer

- Rule-based viral scoring

### Sprint 4 — UI Layer

- Flutter dashboard

### Sprint 5 — Comment Intelligence

- Comment classification

---

## 6. Demo Flow (VERY IMPORTANT)

1. Load VOC / mock data
2. Collector ingests data
3. Analyzer computes metrics
4. Predictor assigns viral score
5. Flutter shows insights

---

## 7. Risks

- VOC schema unknown
- API limits
- Flutter integration complexity
- Time constraints

Mitigation:

- Adapter abstraction layer
- Mock fallback system
- Minimal viable pipeline first

---

## 8. Definition of Success

- End-to-end pipeline runs
- Data flows correctly
- Agents are clearly separated
- Demo narrative is clear
- System works in competition environment

---

## End
This document defines competition execution strategy.