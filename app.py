import streamlit as st
import requests
import json
import os

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="✈️ AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --sand: #F5EDD8;
    --deep: #1A1A2E;
    --teal: #0F7B6C;
    --gold: #C9A84C;
    --warm: #E8D5B7;
    --text: #2C2C3E;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background: linear-gradient(135deg, #F5EDD8 0%, #E8D5B7 50%, #D4C4A0 100%);
    min-height: 100vh;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    background: linear-gradient(160deg, rgba(15,123,108,0.08) 0%, transparent 60%);
    border-radius: 24px;
    margin-bottom: 2rem;
}
.hero h1 {
    font-size: 3.2rem;
    color: var(--deep);
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}
.hero p {
    font-size: 1.15rem;
    color: #5A5A7A;
    font-weight: 300;
}

/* Steps */
.step-bar {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 1.5rem auto 2.5rem;
    max-width: 700px;
    position: relative;
}
.step-bar::before {
    content: '';
    position: absolute;
    top: 22px;
    left: 10%;
    width: 80%;
    height: 2px;
    background: linear-gradient(90deg, var(--teal), var(--gold));
    z-index: 0;
}
.step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    flex: 1;
    z-index: 1;
}
.step-circle {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 600;
    border: 3px solid white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.12);
    transition: all 0.3s;
}
.step-circle.active   { background: var(--teal); color: white; }
.step-circle.done     { background: var(--gold); color: white; }
.step-circle.inactive { background: white; color: #aaa; }
.step-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: #666;
    text-align: center;
    max-width: 80px;
    line-height: 1.3;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    box-shadow: 0 4px 32px rgba(15,123,108,0.08), 0 1px 3px rgba(0,0,0,0.06);
    border: 1px solid rgba(255,255,255,0.8);
    margin-bottom: 1.5rem;
}

/* Profile badges */
.profile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
    margin: 1rem 0;
}
.profile-badge {
    background: linear-gradient(135deg, rgba(15,123,108,0.12), rgba(201,168,76,0.12));
    border: 1px solid rgba(15,123,108,0.2);
    border-radius: 14px;
    padding: 14px 16px;
    text-align: center;
}
.profile-badge .label { font-size: 0.72rem; color: #888; text-transform: uppercase; letter-spacing: 0.06em; }
.profile-badge .value { font-size: 1.05rem; font-weight: 600; color: var(--deep); margin-top: 4px; font-family: 'Playfair Display', serif; }

/* Route display */
.route-day {
    border-left: 3px solid var(--teal);
    padding-left: 1.2rem;
    margin-bottom: 1.4rem;
}
.route-day h4 { color: var(--teal); font-family: 'Playfair Display', serif; margin: 0 0 6px; }

/* Chat */
.chat-msg { margin-bottom: 1rem; }
.chat-msg.user { text-align: right; }
.chat-bubble {
    display: inline-block;
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.5;
}
.user .chat-bubble { background: var(--teal); color: white; border-bottom-right-radius: 4px; }
.assistant .chat-bubble { background: white; color: var(--text); border: 1px solid #e8e8e8; border-bottom-left-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--teal), #0A5C4F) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 15px rgba(15,123,108,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(15,123,108,0.35) !important;
}

/* Inputs */
.stRadio > div { gap: 8px; }
.stSelectbox > div > div, .stTextInput > div > div > input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid rgba(15,123,108,0.2) !important;
    background: rgba(255,255,255,0.8) !important;
}

/* Divider */
hr { border-color: rgba(15,123,108,0.15); margin: 1.5rem 0; }

.tag {
    display: inline-block;
    background: rgba(201,168,76,0.18);
    border: 1px solid rgba(201,168,76,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 500;
    color: #7A5E1A;
    margin: 3px;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
for key, val in {
    "step": 1,
    "answers": {},
    "profile": None,
    "route": None,
    "chat_history": [],
    "q_index": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Questions ───────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": "purpose",
        "text": "Какова главная цель вашей поездки?",
        "type": "radio",
        "options": ["Отдых и релаксация", "Приключения и активный туризм", "Культура и история", "Гастрономия и шопинг", "Цифровой номад / работа"],
        "emoji": "🎯"
    },
    {
        "id": "travel_style",
        "text": "Как вы предпочитаете путешествовать?",
        "type": "radio",
        "options": ["Соло", "С партнёром", "С семьёй (дети)", "С друзьями"],
        "emoji": "👥"
    },
    {
        "id": "duration",
        "text": "Сколько дней займёт поездка?",
        "type": "radio",
        "options": ["2–3 дня (уикенд)", "4–7 дней", "8–14 дней", "Более 2 недель"],
        "emoji": "📅"
    },
    {
        "id": "budget",
        "text": "Ваш бюджет на человека (включая перелёт)?",
        "type": "radio",
        "options": ["До $500", "$500–1500", "$1500–3000", "Свыше $3000", "Гибкий / открытый"],
        "emoji": "💰"
    },
    {
        "id": "destination_hint",
        "text": "Есть ли у вас предпочтения по направлению?",
        "type": "text",
        "placeholder": "Например: Юго-Восточная Азия, Средиземноморье, или совет от ИИ",
        "emoji": "🗺️"
    },
    {
        "id": "accommodation",
        "text": "Предпочтительный тип жилья?",
        "type": "radio",
        "options": ["Хостел / бюджет", "3★ отель", "4–5★ отель", "Апартаменты / Airbnb", "Бутик-отель"],
        "emoji": "🏨"
    },
    {
        "id": "pace",
        "text": "Темп путешествия?",
        "type": "radio",
        "options": ["Медленный (1–2 места глубоко)", "Средний (баланс)", "Быстрый (максимум локаций)"],
        "emoji": "⏱️"
    },
    {
        "id": "interests",
        "text": "Что вас привлекает больше всего? (выберите до 3)",
        "type": "text",
        "placeholder": "Природа, музеи, уличная еда, ночная жизнь, архитектура, пляжи, хайкинг...",
        "emoji": "❤️"
    },
]

# ─── Provider config ─────────────────────────────────────────────────────────
MISTRAL_API_KEY = os.environ["U4Ttbskkzv9xcOl9RQh13AfjsN7kQ49E"]
MISTRAL_URL     = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL   = "mistral-large-latest"

# ─── Helpers ──────────────────────────────────────────────────────────────────
def render_step_bar(current):
    steps = [
        ("🧾", "Опрос"),
        ("🧬", "Профиль"),
        ("💡", "Маршрут"),
        ("💬", "Диалог"),
    ]
    circles = []
    for i, (icon, label) in enumerate(steps, 1):
        if i < current:
            cls = "done"
        elif i == current:
            cls = "active"
        else:
            cls = "inactive"
        circles.append(f"""
        <div class="step-item">
          <div class="step-circle {cls}">{icon}</div>
          <div class="step-label">{label}</div>
        </div>""")
    st.markdown(f'<div class="step-bar">{"".join(circles)}</div>', unsafe_allow_html=True)


def call_llm(system_prompt, user_message, history=None, stream=False):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": MISTRAL_MODEL,
        "max_tokens": 2000,
        "messages": messages,
        "stream": stream,
    }

    if stream:
        with requests.post(MISTRAL_URL, headers=headers, json=payload, stream=True) as resp:
            if not resp.ok:
                st.error(f"Mistral API error {resp.status_code}: {resp.text}")
                return
            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            obj = json.loads(data)
                            delta = obj["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            pass
    else:
        resp = requests.post(MISTRAL_URL, headers=headers, json=payload)
        if not resp.ok:
            st.error(f"Mistral API error {resp.status_code}: {resp.text}")
            return ""
        return resp.json()["choices"][0]["message"]["content"]


def stream_claude(system_prompt, user_message, history=None):
    return call_llm(system_prompt, user_message, history, stream=True)


def build_profile_prompt(answers):
    return f"""Ты — психолог-путешествий и эксперт по туризму. На основе ответов пользователя создай его психологический профиль путешественника.

Ответы пользователя:
{json.dumps(answers, ensure_ascii=False, indent=2)}

Сгенерируй JSON с полями:
- traveler_type: тип путешественника (1–3 слова)
- archetype: архетип (например "Искатель приключений", "Эстет", "Гурман")
- motivation: главная мотивация (1 предложение)
- style: стиль путешествия (1–2 предложения)
- strengths: 3 сильные стороны как путешественника (список)
- challenges: 1–2 возможных сложности в поездке
- perfect_destination_type: идеальный тип направления

Верни ТОЛЬКО валидный JSON без markdown."""


def build_route_prompt(answers, profile):
    return f"""Ты — элитный тревел-консьерж. Создай детализированный маршрут путешествия.

Профиль путешественника:
{json.dumps(profile, ensure_ascii=False, indent=2)}

Предпочтения:
{json.dumps(answers, ensure_ascii=False, indent=2)}

Создай подробный план поездки в формате Markdown с разделами:
## 🗺️ Направление и концепция
## 📅 Маршрут по дням
(для каждого дня: утро/день/вечер с конкретными локациями и активностями)
## 📍 Топ локаций
(5–7 мест с кратким описанием)
## 🍜 Гастрономические точки
(3–5 ресторанов/рынков)
## 💰 Оценка бюджета
(разбивка по категориям)
## 💡 Инсайдерские советы
(3–4 совета)

Будь конкретным: называй реальные места, рестораны, активности."""


# ─── STEP 1: Survey ───────────────────────────────────────────────────────────
def render_survey():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    q_idx = st.session_state.q_index
    total = len(QUESTIONS)

    st.markdown(f"**Вопрос {q_idx + 1} из {total}**")
    progress = (q_idx) / total
    st.progress(progress)

    q = QUESTIONS[q_idx]
    st.markdown(f"### {q['emoji']} {q['text']}")

    answer_key = f"ans_{q['id']}"

    if q["type"] == "radio":
        current = st.session_state.answers.get(q["id"], q["options"][0])
        idx = q["options"].index(current) if current in q["options"] else 0
        val = st.radio("", q["options"], index=idx, key=answer_key, label_visibility="collapsed")
    else:
        current = st.session_state.answers.get(q["id"], "")
        val = st.text_input("", value=current, placeholder=q.get("placeholder", ""), key=answer_key, label_visibility="collapsed")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if q_idx > 0:
            if st.button("← Назад"):
                st.session_state.q_index -= 1
                st.rerun()
    with col3:
        btn_label = "Далее →" if q_idx < total - 1 else "Завершить ✓"
        if st.button(btn_label, type="primary"):
            st.session_state.answers[q["id"]] = val
            if q_idx < total - 1:
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.session_state.step = 2
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ─── STEP 2: Profile ──────────────────────────────────────────────────────────
def render_profile():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🧬 Ваш психологический профиль путешественника")

    if st.session_state.profile is None:
        with st.spinner("Анализируем ваши предпочтения..."):
            prompt = build_profile_prompt(st.session_state.answers)
            try:
                raw = call_llm(
                    "Ты — психолог-путешествий. Отвечай ТОЛЬКО валидным JSON без markdown.",
                    prompt,
                    stream=False,
                )
                raw = raw.replace("```json", "").replace("```", "").strip()
                st.session_state.profile = json.loads(raw)
            except Exception:
                st.session_state.profile = {"traveler_type": "Уникальный путешественник", "archetype": "Исследователь", "motivation": "Открывать новое", "style": "Гибкий и любознательный", "strengths": ["Открытость", "Любопытство", "Адаптивность"], "challenges": ["Сложно выбрать одно место"], "perfect_destination_type": "Разнообразные культурные направления"}

    p = st.session_state.profile
    st.markdown(f"""
    <div class="profile-grid">
      <div class="profile-badge"><div class="label">Тип</div><div class="value">{p.get('traveler_type','—')}</div></div>
      <div class="profile-badge"><div class="label">Архетип</div><div class="value">{p.get('archetype','—')}</div></div>
      <div class="profile-badge"><div class="label">Идеал</div><div class="value">{p.get('perfect_destination_type','—')[:30]}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**🎯 Мотивация:** {p.get('motivation', '')}")
    st.markdown(f"**🧭 Стиль:** {p.get('style', '')}")

    if p.get("strengths"):
        st.markdown("**✨ Сильные стороны:**")
        for s in p["strengths"]:
            st.markdown(f'<span class="tag">✓ {s}</span>', unsafe_allow_html=True)

    if p.get("challenges"):
        st.markdown(f"\n**⚠️ На заметку:** {p['challenges'] if isinstance(p['challenges'], str) else ', '.join(p['challenges'])}")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💡 Сгенерировать маршрут →", type="primary"):
        st.session_state.step = 3
        st.rerun()


# ─── STEP 3: Route ────────────────────────────────────────────────────────────
def render_route():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 💡 Ваш персональный маршрут")

    if st.session_state.route is None:
        with st.spinner("ИИ составляет ваш идеальный маршрут..."):
            prompt = build_route_prompt(st.session_state.answers, st.session_state.profile)
            result = ""
            placeholder = st.empty()
            for chunk in stream_claude(
                "Ты — лучший тревел-консьерж мира. Создавай вдохновляющие и практичные маршруты.",
                prompt
            ):
                result += chunk
                placeholder.markdown(result + "▌")
            placeholder.markdown(result)
            st.session_state.route = result
    else:
        st.markdown(st.session_state.route)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💬 Уточнить маршрут →", type="primary"):
        st.session_state.step = 4
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": f"Ваш маршрут готов! 🎉 Я могу адаптировать его под ваши пожелания. Что хотите изменить или уточнить?"
            }
        ]
        st.rerun()


# ─── STEP 4: Chat ─────────────────────────────────────────────────────────────
def render_chat():
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 💬 Диалоговое уточнение")

        for msg in st.session_state.chat_history:
            role_cls = "user" if msg["role"] == "user" else "assistant"
            icon = "🧳" if msg["role"] == "assistant" else "👤"
            st.markdown(f"""
            <div class="chat-msg {role_cls}">
              <div class="chat-bubble">{icon} {msg['content']}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        user_input = st.text_input(
            "Ваш вопрос или пожелание...",
            placeholder="Добавь больше ресторанов, измени день 3, сколько стоит виза...",
            key="chat_input",
            label_visibility="collapsed"
        )

        if st.button("Отправить →", type="primary") and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            system = f"""Ты — персональный тревел-консьерж. У тебя есть маршрут пользователя:

{st.session_state.route}

Профиль путешественника: {json.dumps(st.session_state.profile, ensure_ascii=False)}

Отвечай кратко и по существу. Если пользователь просит изменить маршрут — предложи конкретные правки."""

            history_for_api = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history[:-1]
            ]

            response_text = ""
            with st.spinner(""):
                for chunk in stream_claude(system, user_input, history_for_api):
                    response_text += chunk

            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            st.rerun()

    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📋 Ваш маршрут")
        if st.session_state.route:
            st.markdown(st.session_state.route[:1200] + "...\n\n*[прокрутите влево для полного маршрута]*" if len(st.session_state.route) > 1200 else st.session_state.route)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔄 Начать заново"):
            for key in ["step", "answers", "profile", "route", "chat_history", "q_index"]:
                del st.session_state[key]
            st.rerun()


# ─── Main ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>✈️ AI Travel Planner</h1>
  <p>Ваш персональный ИИ-консьерж для идеального путешествия</p>
</div>
""", unsafe_allow_html=True)

render_step_bar(st.session_state.step)

if st.session_state.step == 1:
    render_survey()
elif st.session_state.step == 2:
    render_profile()
elif st.session_state.step == 3:
    render_route()
elif st.session_state.step == 4:
    render_chat()
