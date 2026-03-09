# Local AI SOC Agent Setup

## Project Overview
This project documents and stores the working prototype of a **local AI SOC analyst** built using n8n and Ollama. It automates SOC incident analysis using local generative AI.

## Architecture Diagram
Manual Alert → Classification → n8n Workflow → Playbook Selection → Ollama Local AI → SOC Incident Analysis

## Technologies Used
* **n8n**: Workflow automation
* **Ollama**: Local LLM execution
* **gemma:2b model**: AI model used for analysis

## Setup Instructions

### 1. Install and Pull Model
```bash
ollama pull gemma:2b
```

### 2. Run Model
```bash
ollama run gemma:2b
```

### 3. Run n8n
```bash
npx n8n
```

Ensure Ollama API is reachable at: 
`http://127.0.0.1:11434`
