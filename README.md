# 🏗️ Construction Chatbot — Arqonz Assignment

**Assignment Track:** AIML Developer  
**Candidate:** Kaushik Nath (GitHub: [Kaushik-hub18](https://github.com/Kaushik-hub18))  
**Tech Stack:** React (frontend) • FastAPI (backend) • Hosted on Vercel + Render  

---

## 🚀 Live Demo
- **Frontend (Chat UI):** https://construction-chatbot-two.vercel.app  
- **Backend (FastAPI API):** https://construction-chatbot-fh4v.onrender.com  

---

## 📖 Project Description
This is a construction-focused chatbot designed to answer **only construction-related queries**.  
Examples: *“What is curing in concrete?”, “Explain cement types”, “What is scaffolding?”*  

It uses:
- ✅ A curated **rule-based knowledge base** (cement, curing, beams, foundations, rebar, scaffolding, etc.)  
- ✅ **Synonym mapping & typo tolerance** (e.g., “cementing” → “cement”)  
- ✅ **Closest-match suggestion** when queries are unrecognized  
- ✅ **Clickable suggestions** in the frontend  

The chatbot ensures **off-topic queries are not answered**, fulfilling the “construction-only” requirement.

---

## ✨ Features
- Clean React-based chat interface:
  - Auto-scroll to latest message  
  - Typing indicator ⏳  
  - Timestamps for every message  
- Backend (FastAPI):
  - `/chat` endpoint returning construction answers  
  - Synonyms + fuzzy matching via `difflib`  
  - JSON contract: `{ "answer": "<string>" }`  
- Fully deployed:
  - Frontend → **Vercel**  
  - Backend → **Render**  

---

## 🛠️ Architecture
[React Frontend] → POST /chat → [FastAPI Backend] → [Knowledge Base + Logic]

1. User enters a query in the frontend.  
2. Frontend sends POST request to backend `/chat` with body:  
   ```json
   { "query": "What is cement?" }
3. Backend checks keywords, synonyms, and fuzzy matches.

4. Response example: { "answer": "Cement is a binding material used in construction..." }


🧩 Example Usage

User: “What is curing in concrete?”
Bot: “Curing is the process of maintaining adequate moisture, temperature, and time to allow concrete to achieve desired strength and durability.”

User: “Tell me about beams”
Bot: “A beam is a structural member that primarily resists loads applied laterally to the beam's axis.”

🧭 Design Decisions

Rule-based + synonyms ensures safe, domain-specific answers (no off-topic responses).

Fuzzy matching (difflib) improves user experience by handling typos.

Suggestions guide the user back into the supported knowledge base.

🔮 Future Work

Integrate an open-source LLM (e.g., Hugging Face models) wrapped with a retrieval system to expand answers while still restricting to construction domain.

Add database-backed knowledge base (MongoDB) for scalable knowledge storage.

Logging, analytics, and admin dashboard for monitoring.

Screenshots :

<img width="972" height="786" alt="c1" src="https://github.com/user-attachments/assets/5d5cb25e-5793-4af1-8029-aa8f92bab359" />

<img width="957" height="777" alt="c2" src="https://github.com/user-attachments/assets/243d2e97-8cc7-45df-8506-711e8359eb99" />

<img width="962" height="787" alt="c3" src="https://github.com/user-attachments/assets/4615bdb9-056d-4e39-943f-ab0312315422" />

<img width="1037" height="828" alt="c4" src="https://github.com/user-attachments/assets/e4e8645c-0497-4090-85d3-3ff3c7c4b34a" />

