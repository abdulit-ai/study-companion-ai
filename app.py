import streamlit as st
import google.generativeai as genai
import json
import re
import random
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SCHOLAR · AI Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS  — soft forest-green + warm parchment academic aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Nunito:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg:       #f7f4ee;
    --surface:  #efeae0;
    --card:     #ffffff;
    --border:   #d8d0bc;
    --forest:   #2d6a4f;
    --forest2:  #40916c;
    --forest3:  #74c69d;
    --gold:     #b5850a;
    --gold2:    #f0a500;
    --red:      #c1440e;
    --ink:      #1c1a16;
    --ink2:     #3d3826;
    --ink3:     #7a7260;
    --mono:     'Fira Code', monospace;
    --serif:    'Lora', serif;
    --sans:     'Nunito', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--ink) !important;
    font-family: var(--sans) !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton
    { visibility: hidden !important; display: none !important; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
.block-container { padding: 2rem 2.8rem !important; max-width: 1200px !important; }

/* ── Header ── */
.scholar-header {
    background: linear-gradient(135deg, var(--forest) 0%, #1b4332 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.scholar-header::before {
    content: '📚';
    position: absolute; right: 2rem; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem; opacity: 0.12;
}
.scholar-title {
    font-family: var(--serif); font-size: 2.6rem;
    font-weight: 700; color: #fff;
    letter-spacing: -0.01em;
}
.scholar-title span { color: var(--forest3); font-style: italic; }
.scholar-sub {
    font-size: 0.85rem; color: rgba(255,255,255,0.65);
    margin-top: 6px; font-family: var(--mono);
    letter-spacing: 0.05em;
}
.scholar-pills {
    display: flex; gap: 10px; margin-top: 1.2rem; flex-wrap: wrap;
}
.scholar-pill {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px; padding: 4px 14px;
    font-size: 0.75rem; color: rgba(255,255,255,0.85);
    font-family: var(--mono);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 4px !important; gap: 4px !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--sans) !important; font-size: 0.82rem !important;
    font-weight: 600 !important; color: var(--ink3) !important;
    background: transparent !important; border: none !important;
    border-radius: 8px !important; padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--forest) !important; color: white !important;
    box-shadow: 0 2px 8px rgba(45,106,79,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 0 !important; }

/* ── Cards ── */
.tool-card {
    background: var(--card); border: 1.5px solid var(--border);
    border-radius: 16px; padding: 1.6rem;
    box-shadow: 0 2px 12px rgba(28,26,22,0.06);
}
.card-title {
    font-family: var(--serif); font-size: 1.15rem; font-weight: 700;
    color: var(--ink); margin-bottom: 0.2rem;
}
.card-desc { font-size: 0.8rem; color: var(--ink3); margin-bottom: 1.2rem; line-height: 1.5; }

/* ── Flashcard ── */
.flashcard {
    background: linear-gradient(145deg, #fff, var(--surface));
    border: 2px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    min-height: 200px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    box-shadow: 0 8px 24px rgba(28,26,22,0.08);
    position: relative; overflow: hidden;
    animation: cardIn 0.4s ease;
}
@keyframes cardIn {
    from { opacity: 0; transform: scale(0.96) translateY(8px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}
.flashcard::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, var(--forest), var(--gold2));
}
.flashcard-num {
    font-family: var(--mono); font-size: 0.65rem;
    color: var(--ink3); letter-spacing: 0.15em; margin-bottom: 1rem;
}
.flashcard-q {
    font-family: var(--serif); font-size: 1.25rem; font-weight: 600;
    color: var(--ink); line-height: 1.5; margin-bottom: 1rem;
}
.flashcard-a {
    font-size: 0.92rem; color: var(--forest);
    background: rgba(45,106,79,0.08);
    border: 1px solid rgba(45,106,79,0.2);
    border-radius: 10px; padding: 12px 20px;
    line-height: 1.6; margin-top: 0.5rem;
}

/* ── Quiz option ── */
.quiz-option {
    background: var(--card); border: 1.5px solid var(--border);
    border-radius: 10px; padding: 12px 18px;
    margin-bottom: 8px; cursor: pointer;
    font-size: 0.9rem; color: var(--ink2);
    transition: all 0.15s;
}
.quiz-option:hover { border-color: var(--forest2); background: rgba(45,106,79,0.04); }
.quiz-correct { border-color: var(--forest) !important; background: rgba(45,106,79,0.08) !important; color: var(--forest) !important; }
.quiz-wrong   { border-color: var(--red) !important; background: rgba(193,68,14,0.06) !important; color: var(--red) !important; }

/* ── Score badge ── */
.score-badge {
    display: inline-block;
    background: var(--forest); color: white;
    font-family: var(--mono); font-size: 0.75rem;
    padding: 4px 14px; border-radius: 20px;
    margin-bottom: 1rem;
}

/* ── Output ── */
.output-panel {
    background: var(--card); border: 1.5px solid var(--border);
    border-left: 4px solid var(--forest);
    border-radius: 0 14px 14px 0;
    padding: 1.5rem 1.8rem; margin-top: 1.2rem;
    font-size: 0.9rem; line-height: 1.8; color: var(--ink2);
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.output-label {
    font-family: var(--mono); font-size: 0.62rem;
    color: var(--forest); letter-spacing: 0.15em;
    text-transform: uppercase; margin-bottom: 10px;
}

/* ── Progress bar ── */
.prog-wrap {
    background: var(--border); border-radius: 6px;
    height: 8px; margin: 8px 0;
    overflow: hidden;
}
.prog-fill {
    height: 100%; border-radius: 6px;
    background: linear-gradient(90deg, var(--forest), var(--forest3));
    transition: width 0.4s ease;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
    font-family: var(--sans) !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--forest) !important;
    box-shadow: 0 0 0 3px rgba(45,106,79,0.12) !important;
}
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--forest) !important; color: white !important;
    border: none !important; border-radius: 10px !important;
    font-family: var(--sans) !important; font-weight: 700 !important;
    font-size: 0.88rem !important; padding: 0.55rem 1.5rem !important;
    box-shadow: 0 4px 12px rgba(45,106,79,0.25) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--forest2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(45,106,79,0.35) !important;
}

/* ── Sidebar ── */
.stSlider [data-baseweb="slider"] div[role="slider"] { background: var(--forest) !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for k, v in {
    "api_ready": False,
    "flashcards": [],
    "fc_index": 0,
    "fc_show_answer": False,
    "quiz_questions": [],
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_answered": False,
    "quiz_selected": None,
    "notes_history": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 SCHOLAR Settings")
    st.markdown("---")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="AIza…")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.api_ready = True
            st.success("✓ Connected", icon="🟢")
        except Exception:
            st.error("Invalid key")

    st.markdown("---")
    model_choice = st.selectbox("Model", ["gemini-2.5-flash", "gemini-2.5-pro"])
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    num_items = st.slider("Items to generate", 3, 15, 6)

    st.markdown("---")
    st.metric("Flashcards", len(st.session_state.flashcards))
    st.metric("Quiz Questions", len(st.session_state.quiz_questions))
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.flashcards = []
        st.session_state.quiz_questions = []
        st.session_state.fc_index = 0
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def gemini(prompt: str, system: str = "") -> str:
    if not st.session_state.api_ready:
        return "⚠️ Add your Gemini API key in the sidebar."
    try:
        model = genai.GenerativeModel(
            model_choice,
            system_instruction=system or "You are SCHOLAR, an expert academic tutor. Be clear, accurate, and pedagogically sound.",
            generation_config=genai.GenerationConfig(temperature=0.5, max_output_tokens=2048),
        )
        return model.generate_content(prompt).text
    except Exception as e:
        return f"⚠️ Error: {e}"


def parse_json_response(text: str) -> list:
    """Extract JSON array from LLM response."""
    try:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return []


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="scholar-header">
  <div class="scholar-title">SCHOLAR <span>AI</span></div>
  <div class="scholar-sub">YOUR INTELLIGENT STUDY COMPANION · POWERED BY GEMINI</div>
  <div class="scholar-pills">
    <span class="scholar-pill">📇 Flashcards</span>
    <span class="scholar-pill">❓ Quizzes</span>
    <span class="scholar-pill">📝 Notes</span>
    <span class="scholar-pill">🗺️ Mind Maps</span>
    <span class="scholar-pill">🔍 Explainer</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📇 Flashcards", "❓ Quiz", "📝 Smart Notes", "🗺️ Mind Map", "🔍 Explainer", "📊 Summarise"])

# ══════════════════════════════════════════════════════
# TAB 1 — FLASHCARDS
# ══════════════════════════════════════════════════════
with tabs[0]:
    col_gen, col_view = st.columns([1, 1], gap="large")

    with col_gen:
        st.markdown('<div class="tool-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Generate Flashcards</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Paste notes or enter a topic to auto-generate study flashcards.</div>', unsafe_allow_html=True)
        topic = st.text_area("Topic or paste your notes", height=140,
                             placeholder="e.g. The water cycle, or paste lecture notes…")
        if st.button("Generate Flashcards 📇", key="fc_gen"):
            if not topic.strip():
                st.warning("Enter a topic or notes.")
            else:
                with st.spinner("Generating flashcards…"):
                    prompt = f"""Generate {num_items} flashcards at {difficulty} level for the following topic/notes.
Return ONLY a JSON array like:
[{{"question": "...", "answer": "..."}}]
No extra text, no markdown fences.

Topic/Notes:
{topic}"""
                    raw = gemini(prompt)
                    cards = parse_json_response(raw)
                    if cards:
                        st.session_state.flashcards = cards
                        st.session_state.fc_index = 0
                        st.session_state.fc_show_answer = False
                        st.success(f"✓ {len(cards)} flashcards generated!")
                        st.rerun()
                    else:
                        st.error("Could not parse flashcards. Try again.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_view:
        if st.session_state.flashcards:
            cards = st.session_state.flashcards
            idx = st.session_state.fc_index
            card = cards[idx]
            total = len(cards)

            st.markdown(f'<div class="score-badge">Card {idx+1} of {total}</div>', unsafe_allow_html=True)
            progress = (idx + 1) / total * 100
            st.markdown(f'<div class="prog-wrap"><div class="prog-fill" style="width:{progress}%"></div></div>', unsafe_allow_html=True)

            show = st.session_state.fc_show_answer
            answer_html = f'<div class="flashcard-a">💡 {card["answer"]}</div>' if show else ""
            st.markdown(f"""
            <div class="flashcard">
                <div class="flashcard-num">QUESTION {idx+1} · {difficulty.upper()}</div>
                <div class="flashcard-q">{card['question']}</div>
                {answer_html}
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("👁 Show Answer", key="fc_show"):
                    st.session_state.fc_show_answer = not st.session_state.fc_show_answer
                    st.rerun()
            with c2:
                if st.button("⟵ Prev", key="fc_prev") and idx > 0:
                    st.session_state.fc_index -= 1
                    st.session_state.fc_show_answer = False
                    st.rerun()
            with c3:
                if st.button("Next ⟶", key="fc_next") and idx < total - 1:
                    st.session_state.fc_index += 1
                    st.session_state.fc_show_answer = False
                    st.rerun()

            # Export
            export_txt = "\n\n".join(f"Q: {c['question']}\nA: {c['answer']}" for c in cards)
            st.download_button("⬇ Export Flashcards", data=export_txt,
                               file_name="flashcards.txt", mime="text/plain")
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:var(--ink3);">
                <div style="font-size:3rem">📇</div>
                <div style="font-family:'Fira Code',monospace;font-size:0.8rem;margin-top:8px;">
                    Generate flashcards to start studying
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 2 — QUIZ
# ══════════════════════════════════════════════════════
with tabs[1]:
    col_qgen, col_qplay = st.columns([1, 1], gap="large")

    with col_qgen:
        st.markdown('<div class="tool-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Generate Quiz</div>', unsafe_allow_html=True)
        quiz_topic = st.text_area("Topic or notes for quiz", height=120,
                                   placeholder="e.g. Photosynthesis, World War II, Python basics…")
        quiz_type = st.selectbox("Question type", ["Multiple choice (4 options)", "True / False"])
        if st.button("Generate Quiz ❓", key="quiz_gen"):
            if not quiz_topic.strip():
                st.warning("Enter a topic.")
            else:
                with st.spinner("Generating quiz…"):
                    if "Multiple choice" in quiz_type:
                        prompt = f"""Generate {num_items} multiple-choice quiz questions at {difficulty} level.
Return ONLY a JSON array:
[{{"question":"...","options":["A)...","B)...","C)...","D)..."],"answer":"A)..."}}]
No extra text.

Topic: {quiz_topic}"""
                    else:
                        prompt = f"""Generate {num_items} True/False quiz questions at {difficulty} level.
Return ONLY a JSON array:
[{{"question":"...","options":["True","False"],"answer":"True"}}]
No extra text.

Topic: {quiz_topic}"""
                    raw = gemini(prompt)
                    qs = parse_json_response(raw)
                    if qs:
                        st.session_state.quiz_questions = qs
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_score = 0
                        st.session_state.quiz_answered = False
                        st.session_state.quiz_selected = None
                        st.success(f"✓ {len(qs)} questions ready!")
                        st.rerun()
                    else:
                        st.error("Could not parse questions. Try again.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_qplay:
        if st.session_state.quiz_questions:
            qs = st.session_state.quiz_questions
            qi = st.session_state.quiz_index

            if qi >= len(qs):
                # Results screen
                score = st.session_state.quiz_score
                total = len(qs)
                pct = int(score / total * 100)
                grade = "🏆 Excellent!" if pct >= 80 else "👍 Good" if pct >= 60 else "📖 Keep Studying"
                st.markdown(f"""
                <div class="flashcard">
                    <div class="flashcard-num">QUIZ COMPLETE</div>
                    <div class="flashcard-q" style="font-size:2rem">{grade}</div>
                    <div class="flashcard-a">{score}/{total} correct · {pct}%</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔄 Restart Quiz"):
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
                    st.rerun()
            else:
                q = qs[qi]
                total = len(qs)
                progress = qi / total * 100
                st.markdown(f'<div class="score-badge">Q{qi+1}/{total} · Score: {st.session_state.quiz_score}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prog-wrap"><div class="prog-fill" style="width:{progress}%"></div></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="flashcard" style="min-height:120px;">
                    <div class="flashcard-num">QUESTION {qi+1}</div>
                    <div class="flashcard-q">{q['question']}</div>
                </div>
                """, unsafe_allow_html=True)

                answered = st.session_state.quiz_answered
                selected = st.session_state.quiz_selected
                correct = q.get("answer", "")

                for opt in q.get("options", []):
                    css = ""
                    if answered:
                        if opt == correct:
                            css = "quiz-correct"
                        elif opt == selected and opt != correct:
                            css = "quiz-wrong"
                    st.markdown(f'<div class="quiz-option {css}">{opt}</div>', unsafe_allow_html=True)
                    if not answered:
                        if st.button(f"Select: {opt[:40]}", key=f"opt_{qi}_{opt[:20]}"):
                            st.session_state.quiz_selected = opt
                            st.session_state.quiz_answered = True
                            if opt == correct:
                                st.session_state.quiz_score += 1
                            st.rerun()

                if answered:
                    if st.button("Next Question ⟶", key="quiz_next"):
                        st.session_state.quiz_index += 1
                        st.session_state.quiz_answered = False
                        st.session_state.quiz_selected = None
                        st.rerun()

# ══════════════════════════════════════════════════════
# TAB 3 — SMART NOTES
# ══════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Smart Notes Enhancer</div>', unsafe_allow_html=True)
    raw_notes = st.text_area("Paste your rough notes", height=180,
                              placeholder="Paste messy lecture notes, voice-to-text dumps, or bullet points…")
    c1, c2 = st.columns(2)
    with c1:
        notes_style = st.selectbox("Output format", [
            "Structured notes with headings",
            "Cornell notes format",
            "Numbered outline",
            "Study guide",
            "Key definitions list",
        ])
    with c2:
        notes_action = st.selectbox("Enhancement", [
            "Clean & organise",
            "Expand with examples",
            "Add memory tips",
            "Highlight key concepts",
            "Add practice questions",
        ])
    if st.button("Enhance Notes 📝", key="notes_btn"):
        if not raw_notes.strip():
            st.warning("Paste your notes first.")
        else:
            with st.spinner("Enhancing notes…"):
                prompt = f"""Take the following student notes and enhance them.
Format: {notes_style}
Enhancement: {notes_action}
Level: {difficulty}
Make them clear, well-organised, and study-ready.

Raw Notes:
{raw_notes}"""
                result = gemini(prompt, "You are an expert academic note-taker and study skills coach.")
            st.markdown(f'<div class="output-panel"><div class="output-label">Enhanced Notes</div>{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
            st.download_button("⬇ Download Notes", data=result, file_name="enhanced_notes.md", mime="text/markdown")
            st.session_state.notes_history.append({"input": raw_notes[:100], "output": result, "time": datetime.now().strftime("%H:%M")})
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 4 — MIND MAP
# ══════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Mind Map Generator</div>', unsafe_allow_html=True)
    mm_topic = st.text_input("Central topic", placeholder="e.g. Machine Learning, The French Revolution…")
    mm_depth = st.slider("Depth (branches)", 2, 5, 3)
    if st.button("Generate Mind Map 🗺️", key="mm_btn"):
        if not mm_topic.strip():
            st.warning("Enter a topic.")
        else:
            with st.spinner("Building mind map…"):
                prompt = f"""Create a detailed mind map for the topic: "{mm_topic}"
Difficulty: {difficulty}. Depth: {mm_depth} levels.

Format as a structured text mind map using indentation and symbols:
🔵 {mm_topic}
  ├── 🟢 Branch 1
  │     ├── 📌 Sub-point 1.1
  │     └── 📌 Sub-point 1.2
  ├── 🟢 Branch 2
  ...

Use emojis to distinguish levels. Be comprehensive but concise."""
                result = gemini(prompt)
            st.markdown(f'<div class="output-panel"><div class="output-label">Mind Map — {mm_topic}</div><pre style="font-family:\'Fira Code\',monospace;font-size:0.85rem;white-space:pre-wrap;color:var(--ink2)">{result}</pre></div>', unsafe_allow_html=True)
            st.download_button("⬇ Download Mind Map", data=result, file_name="mind_map.txt", mime="text/plain")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 5 — EXPLAINER
# ══════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Concept Explainer</div>', unsafe_allow_html=True)
    explain_topic = st.text_input("Concept to explain", placeholder="e.g. Recursion, Entropy, DNA replication…")
    explain_style = st.selectbox("Explanation style", [
        "Simple (like I'm 10)", "With analogy", "Technical deep-dive",
        "Step-by-step", "With real-world examples", "Historical context",
    ])
    if st.button("Explain 🔍", key="explain_btn"):
        if not explain_topic.strip():
            st.warning("Enter a concept.")
        else:
            with st.spinner("Explaining…"):
                prompt = f"""Explain "{explain_topic}" at {difficulty} level using the style: {explain_style}.
Be thorough, clear, and engaging. Use examples, analogies, or diagrams (as ASCII/text) where helpful."""
                result = gemini(prompt)
            st.markdown(f'<div class="output-panel"><div class="output-label">Explanation: {explain_topic}</div>{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
            st.download_button("⬇ Download Explanation", data=result, file_name="explanation.md", mime="text/markdown")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 6 — SUMMARISE
# ══════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Study Summariser</div>', unsafe_allow_html=True)
    summ_text = st.text_area("Paste lecture / chapter text", height=200,
                              placeholder="Paste a chapter, article, or lecture transcript…")
    summ_output = st.selectbox("Output type", [
        "Concise summary", "Key points only", "Exam-ready revision notes",
        "Important definitions", "Timeline (for history)", "Formula sheet (for STEM)",
    ])
    if st.button("Summarise 📊", key="summ_btn"):
        if not summ_text.strip():
            st.warning("Paste some text first.")
        else:
            with st.spinner("Summarising…"):
                prompt = f"""Summarise the following academic content.
Output type: {summ_output}
Level: {difficulty}
Make it exam-focused, accurate, and easy to review.

Content:
{summ_text[:8000]}"""
                result = gemini(prompt)
            st.markdown(f'<div class="output-panel"><div class="output-label">{summ_output}</div>{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
            st.download_button("⬇ Download Summary", data=result, file_name="summary.md", mime="text/markdown")
    st.markdown('</div>', unsafe_allow_html=True)
