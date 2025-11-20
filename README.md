# AbuelAI

AbuelAI is a personal project born from a simple but powerful motivation: helping my grandma, Mimi. Like many older adults, she often struggles to understand how to use streaming platforms, configure accounts, or troubleshoot basic issues on digital devices. This project is my attempt to make technology feel a little less overwhelming for her — and hopefully for others facing similar challenges.

AbuelAI is a lightweight, local-first agent designed to retrieve step-by-step instructions from structured help data, PDFs, and scraped platform documentation. It combines rule-based planning, a memory layer, and tools for retrieving information from chunked datasets.

---

## Features

- Conversational agent designed to simplify technical explanations
- Retrieval of help instructions from CSVs, JSON knowledge bases, and PDFs
- Lightweight planning system to decide which tool or data source to use
- Memory module to keep track of conversation state
- Optional embedding flow for vector databases
- Scrapers and data-preparation utilities for major streaming platforms
- Runs with a clean, modular Python structure

---

## Project Structure

```
agent/
│── config.py
│── main.py
│── memory.py
│── planning.py
└── tools.py

data/
│── processed_data/
│     ├── max_help.csv
│     ├── netflix_help.csv
│     └── prime_help.csv
│
└── raw_data/
      ├── Manual_Uso_Tecnologico.pdf
      └── tecnologia_edades_Digital.pdf

json_database/
│── max_db.json
│── max_db_2.json
│── netflix_db.json
│── netflix_db_2.json
│── prime_db.json
└── primex_db_2.json

src/
│── chromedriver.exe
│
├── chunking/
│     ├── create_db.py
│     └── rqst_db.py
│
├── embedding/
│     ├── create_vector_db.py
│     └── embedding.py
│
└── scrapping/
      ├── disney_scrapping.py
      ├── hbo_scrapping.py
      ├── netflix_scrapping.py
      ├── prime_scarpping.py
      └── rqst_scrapping.py
```

---

## Architecture

```
                               ┌──────────────────────────┐
                               │        User Input        │
                               └─────────────┬────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │        agent/main.py          │
                              │  (Main Orchestrator Loop)     │
                              └─────────────┬────────────────┘
                                             │
                                Selects next action via
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │     agent/planning.py         │
                              │  (Routing & Agent Logic)      │
                              └─────────────┬────────────────┘
                                             │
                              Determines whether it needs:
                              - memory
                              - tools
                              - data retrieval
                              - scraping/db content
                                             │
                                             ▼
     ┌───────────────────────────────┐     ┌──────────────────────────────┐
     │       agent/memory.py         │     │        agent/tools.py         │
     │  (Conversation State, History)│     │  (Utilities: fetch CSV,      │
     │                               │     │   retrieve JSON chunks, etc.)│
     └──────────────┬────────────────┘     └──────────────┬──────────────┘
                    │                                     │
                    │                                     │
                    └──────────────────────┬──────────────┘
                                           │
                                           ▼
                   ┌────────────────────────────────────────────────┐
                   │            Data Retrieval Layer                 │
                   └───────────────────────┬────────────────────────┘
                                           │
                                           ▼
          ┌──────────────────────────────┬────────────────────────────────────┐
          │                              │                                    │
          ▼                              ▼                                    ▼
┌──────────────────────┐    ┌────────────────────────┐            ┌────────────────────────┐
│  data/processed_data  │    │     json_database      │            │  src/embedding/*.py     │
│  *.csv (help content) │    │  *.json (chunked data) │            │  (vector DB utilities)   │
└──────────────────────┘    └────────────────────────┘            └────────────────────────┘

                                           │
                                           ▼
                          ┌────────────────────────────────┐
                          │   agent builds final response   │
                          │  (formatting, simplification)   │
                          └────────────────┬───────────────┘
                                           │
                                           ▼
                                ┌─────────────────────────┐
                                │       User Output       │
                                └─────────────────────────┘
```

---

## Installation

### 1. Clone the repo

```
git clone https://github.com/julilc/abuelAI.git
cd abuelAI
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. (Optional) Configure MongoDB Atlas

```
export MONGO_URI="your_mongo_connection_string"
export MONGO_DB="abuelai"
```

---

## Running the Agent

```
python agent/main.py
```

---

## Contributions

Any comments or contributions feel free to reach me:
https://www.linkedin.com/in/julietalc/

