
ai-document-intelligence/
│
├── frontend/                  # Next.js UI (later)
│
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── documents.py       # PDF upload and text extraction
│   │   └── rag.py             # Chunking, retrieval and AI (later)
│   │
│   ├── tests/                 # Automated tests (when needed)
│   ├── .venv/                 # Local Python environment
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # API keys (never commit)
│
├── data/                      # Sample PDFs for testing
├── README.md                  # Project overview
└── .gitignore
