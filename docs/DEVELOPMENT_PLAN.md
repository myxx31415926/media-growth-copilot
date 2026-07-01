# 📘 DEVELOPMENT_PLAN — Sprint 1

## 🎯 Goal
Build end-to-end data flow using Adapter → Collector → Output

---

## 🧩 Task 1: Adapter Layer

- Create BaseAdapter
- Create CSVAdapter
- Create VOCAdapter (mock placeholder)

---

## 🧩 Task 2: Collector Agent

- Read data from adapter
- Normalize to video schema
- Return ingestion report

---

## 🧩 Task 3: Run Pipeline

- main.py entry point
- Execute collector
- Print result

---

## 🧪 Success Criteria

- CSV loads successfully
- Collector returns structured output
- No runtime errors
- No AI logic yet

---

## 🚫 Do NOT do

- No Analyzer
- No Predictor
- No Flutter
- No SQLite