# 🎨 Figma to Code Generator (Ollama + DeepSeek)

> Convert Figma designs into clean, responsive HTML/CSS using AI — powered by FastAPI, Streamlit, and DeepSeek.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![LLM](https://img.shields.io/badge/LLM-DeepSeek-orange)
![Status](https://img.shields.io/badge/Status-Working-success)

---

## 📌 Overview

This is a **full-stack AI-powered application** that bridges:

* 🎨 **Figma Designs**
* ⚙️ **Backend APIs (FastAPI)**
* 💬 **Interactive UI (Streamlit)**
* 🤖 **LLMs (DeepSeek via Ollama)**

It allows you to:

* Extract UI layouts from Figma
* Understand design structure
* Generate **production-ready HTML/CSS**
* Iteratively refine code via chat

---

## ✨ Features

* 🎨 **Direct Figma Integration**
  Fetch document structure and UI nodes using Figma API

* 🧠 **Intelligent Code Generation**
  Converts design elements into semantic HTML + Flexbox/Grid CSS

* 💬 **Interactive Chat Interface**
  Ask follow-ups, refine layouts, tweak UI in real-time

* 🎯 **Code Highlighting**
  Clean syntax-highlighted HTML/CSS in chat output

---

## 🧠 Architecture

```
Figma API  →  FastAPI Backend  →  DeepSeek (Ollama)
                    ↓
              Streamlit UI
                    ↓
               User Interaction
```

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **LLM Engine:** DeepSeek (via Ollama Cloud)
* **Design API:** Figma REST API
* **Environment Management:** python-dotenv

---

## 📦 Installation

### 1. Clone the repository

```powershell
git clone https://github.com/MusW02/figma-ollama-chat-interface.git
cd figma-ollama-chat-interface
```

### 2. Create virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 🔑 Create `.env` file

```env
# API Keys
FIGMA_ACCESS_TOKEN=your_figma_token_here
OLLAMA_API_KEY=your_ollama_key_here

# Model Config
OLLAMA_MODEL=deepseek-v3.1:671b-cloud
OLLAMA_ENDPOINT=https://ollama.com/api/generate
```

⚠️ Make sure `.env` is added to `.gitignore` to keep your keys safe.

---

## 🚀 Running the Application

Since this is a **full-stack app**, run backend and frontend separately.

---

### 🖥️ Terminal 1 — Start Backend (FastAPI)

```powershell
.\venv\Scripts\activate
python backend.py
```

📍 Runs on: http://localhost:8000

---

### 🌐 Terminal 2 — Start Frontend (Streamlit)

```powershell
.\venv\Scripts\activate
streamlit run frontend.py
```

📍 Opens automatically at: http://localhost:8501

---

## 💡 Usage Guide

1. Open the Streamlit interface
2. Paste your **Figma File ID** (from URL)
3. Click **"Generate Code from Figma"**

Behind the scenes:

* Fetches design tree (`?depth=1`)
* Parses nodes (frames, text, styles)
* Sends structured prompt to DeepSeek
* Returns clean HTML/CSS

💬 You can then:

* Ask for improvements
* Change layout
* Modify styling

---

## ⚠️ Figma Rate Limits

Figma may return **HTTP 429 (Too Many Requests)** if you spam requests.

✔️ This project mitigates it using:

* `?depth=1` (smaller payloads)

❗ Still avoid rapid repeated clicks during testing.

---

## 🎯 Use Cases

* Convert **Figma → Frontend instantly**
* Build **AI-powered UI generators**
* Speed up **frontend workflows**
* Learn **LLM + Full-stack integration**

---

## 🚀 Future Improvements

* [ ] React / Next.js code generation
* [ ] Tailwind CSS support
* [ ] Multi-page Figma parsing
* [ ] Live preview panel
* [ ] Docker deployment

---

## 📂 Project Structure

```
figma-ollama-chat-interface/
│
├── backend.py        # FastAPI server
├── frontend.py       # Streamlit UI
├── requirements.txt  # Dependencies
├── .env              # Secrets (ignored)
├── .gitignore        # Ignore rules
└── README.md         # Documentation
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a branch
3. Submit a PR

---

## ⭐ Support

If you found this useful:

* ⭐ Star the repo
* 🍴 Fork it
* 📢 Share it

---

## 👨‍💻 Author

**Mustafa Waqar**
Aspiring ML Engineer | AI & Data Science

---

## 🚀 Push to GitHub

```powershell
git add README.md
git commit -m "docs: add professional README for full-stack figma code generator"
git push origin main
```
