# RAG Pipeline Backend

## 📚 Overview
Backend for RAG Chatbot integrated with Physical AI & Humanoid Robotics book.

## 🛠️ Tech Stack
- **FastAPI** - REST API framework
- **OpenAI Agent SDK** - Agent orchestration
- **Cohere** - Embeddings generation
- **Qdrant** - Vector database
- **Groq** - LLM inference

## 📦 Installation

### 1. Clone Repository
\`\`\`bash
git clone <your-repo-url>
cd rag_pipeline
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
python -m venv .venv
.venv\Scripts\activate  # Windows
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Environment Variables
\`\`\`bash
cp .env.example .env
# Edit .env with your API keys
\`\`\`

## 🚀 Usage

### Start API Server
\`\`\`bash
python api.py
\`\`\`

Server will run on: `http://localhost:8000`

### API Endpoints
- **GET** `/health` - Health check
- **POST** `/ask` - Ask questions

### Example Request
\`\`\`bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?"}'
\`\`\`

## 📁 Project Structure
\`\`\`
rag_pipeline/
├── agent.py          # RAG Agent implementation
├── api.py            # FastAPI application
├── retrieval.py      # Vector search & retrieval
├── requirements.txt  # Python dependencies
└── .env.example      # Environment variables template
\`\`\`

## 🔑 Required API Keys
- Groq API Key (LLM)
- Cohere API Key (Embeddings)
- Qdrant Cloud credentials

## 📝 License
MIT License
\`\`\`

---

## 🎯 **Complete Upload Commands:**
```powershell
# 1. Navigate to project root
cd C:\Users\DEll\textbook

# 2. Check status
git status

# 3. Add rag_pipeline files
git add rag_pipeline/agent.py
git add rag_pipeline/api.py
git add rag_pipeline/requirements.txt
git add rag_pipeline/retrieval.py
git add rag_pipeline/.env.example
git add rag_pipeline/README.md

# 4. Commit
git commit -m "✅ Add RAG Pipeline Backend

- Implement RAG Agent with OpenAI SDK
- Create FastAPI endpoints
- Add retrieval system with Qdrant
- Include environment template
- Add documentation"

# 5. Push to GitHub
git push origin main
```