# media-growth-copilot
An AI-powered media operations agent for content analytics, viral prediction, and comment assistance...
## 1. Product Vision

Media Growth Copilot is an AI-powered media operations system that helps content and marketing teams:

- Automatically collect content performance data from social platforms (YouTube / Instagram)
- Identify early-stage viral content signals
- Generate structured performance insights
- Assist in comment classification and response suggestions
- Push key signals to Feishu for real-time operations monitoring

The goal is to reduce manual data processing and enable faster content iteration cycles.

## 2. System Overview

The system consists of four main layers:

### 1. Data Collection Layer
- Pulls video/content data from platforms (initially CSV / mock data, later APIs)

### 2. Storage Layer
- Stores structured content data in SQLite database

### 3. Intelligence Layer
- Computes engagement metrics
- Predicts viral probability
- Generates insights and anomaly detection

### 4. Action Layer
- Sends alerts to Feishu
- Provides comment classification and reply suggestions

## 3. Data Sources

Initial phase:
- YouTube sample dataset (provided by team)
- Instagram mock/export data

Future phase:
- YouTube Data API
- Instagram Graph API
- Third-party analytics tools

## 4. Core Agents

### 1. Collector Agent
Responsible for ingesting content data from external sources.

### 2. Analyzer Agent
Computes:
- Engagement Rate
- View Growth Rate
- Like/Comment Ratio

### 3. Predictor Agent
Outputs:
- Viral probability score (0-100)
- Content potential classification

### 4. Comment Agent
Handles:
- Comment classification
- Reply suggestions
- Risk detection (negative / support / spam / sales inquiry)

## 5. Data Model

### Video Table
- video_id
- platform
- title
- publish_time
- views
- likes
- comments
- shares
- engagement_rate
- viral_score
- created_at

### Comment Table
- comment_id
- video_id
- content
- sentiment
- category
- reply_suggestion
- risk_level

## 6. Workflows

1. Data is collected via Collector Agent
2. Stored in SQLite database
3. Analyzer computes engagement metrics
4. Predictor generates viral score
5. Feishu receives:
   - High potential videos
   - Anomalies
   - Weekly summary
6. Comment Agent processes new comments and generates suggestions

## 7. Rules & Principles

### 1. Modularity First
Each Agent must be independent and replaceable.

### 2. No Hard Dependency on APIs
System must work with mock data first.

### 3. Observability
All outputs must be traceable (logs / tables).

### 4. Human-in-the-loop
No fully autonomous actions in comment posting.

### 5. Incremental Complexity
Start simple → add intelligence gradually.

### 6. Codex-Ready Design
All modules must be structured so Codex can implement them independently.