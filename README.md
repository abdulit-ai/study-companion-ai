# 🎓 SCHOLAR — AI Study Companion

> **Six study tools in one app.** Flashcards, quizzes, smart notes, mind maps, concept explainer, and summariser — all powered by Google Gemini.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-API-orange?style=flat-square)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## Overview

SCHOLAR is an AI-powered study companion that transforms any topic or lecture notes into interactive study materials in seconds. Built for students who want to study smarter, not harder.

---

## Tools

| Tab | Tool | Description |
|---|---|---|
| 📇 | **Flashcards** | Auto-generate Q&A flashcards from any topic or notes. Navigate with prev/next, reveal answers, export as TXT |
| ❓ | **Quiz** | Multiple-choice or True/False quizzes with live scoring and progress tracking |
| 📝 | **Smart Notes** | Paste messy notes → get structured Cornell notes, outlines, or study guides |
| 🗺️ | **Mind Map** | Generate hierarchical text mind maps with configurable depth |
| 🔍 | **Explainer** | Explain any concept — simple, technical, with analogy, or step-by-step |
| 📊 | **Summariser** | Condense lectures into revision notes, key points, formula sheets, or timelines |

---

## Getting Started

```bash
git clone https://github.com/<your-username>/study-companion-ai.git
cd study-companion-ai
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Enter your Gemini API key in the sidebar when the app loads.

---

## Key Features

- **Difficulty control** — Beginner / Intermediate / Advanced modes affect all generated content
- **JSON prompt engineering** — Flashcards and quiz questions are returned as structured JSON for reliable parsing
- **Exportable outputs** — Every tool has a download button (TXT or Markdown)
- **Session state** — Flashcard position and quiz score persist across interactions
- **Forest-green academic design** — Lora serif + Nunito sans + Fira Code mono typography

---

## Deployment

```
1. Push to GitHub
2. share.streamlit.io → connect repo → deploy
```

Live URL format: `https://study-companion-ai.streamlit.app`

---

## Author

**Abdurrahman Abdulazeez** · abdulitz95@gmail.com · Kaduna, Nigeria

---

## License

MIT
