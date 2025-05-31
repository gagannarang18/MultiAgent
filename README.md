# Multi-Agent AI System for Intelligent Document Processing

## Overview

This project implements a multi-agent AI system that classifies input formats and intents from various document types (PDF, JSON, Email) and routes them to specialized agents for processing. The system maintains a shared memory module to ensure traceability and context sharing across agents.

---

## Architecture

### 1. Classifier Agent
- **Input**: Raw file (PDF/JSON/Email)
- **Function**:
  - Detects input format (PDF, JSON, Email)
  - Determines intent (e.g., Invoice, RFQ, Complaint, Regulation)
  - Routes to the appropriate agent
  - Logs classification info into shared memory

### 2. JSON Agent
- **Input**: Structured JSON payload
- **Function**:
  - Extracts and reformats to a target schema
  - Flags missing or anomalous fields

### 3. Email Agent
- **Input**: Email text
- **Function**:
  - Extracts sender, intent, and urgency
  - Formats output for CRM-style consumption

### 4. Shared Memory Module
- **Stores**:
  - Extracted fields
  - Source, format, intent
  - Timestamp
  - Thread or conversation ID
- **Implementation**: In-memory/Redis/SQLite (configurable)

---

## Example Workflow

1. User sends an Email.
2. Classifier Agent detects format (`Email`) and intent (`RFQ`).
3. Routes to Email Agent.
4. Email Agent extracts fields (sender, urgency, etc.).
5. Shared memory logs result with timestamp and thread ID.

---

## Tech Stack

- **Language**: Python
- **Models**: Open-source LLMs(Groq cloud)
- **Memory**:  SQLite 

---

## Demo

📽️ **[Watch the demo video](demo_video_link)**  
📷 **Screenshots** available in the `demo_screenshots/` folder.

---


## How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/gagannarang18/MultiAgent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the system:
   ```bash
   python main.py --input path/to/file_or_text
   ```

---
