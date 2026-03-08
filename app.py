import streamlit as st
import requests
import json
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🌍 AI Travel Guide",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — luxury dark travel aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --gold: #C9A84C;
    --gold-light: #E8C97A;
    --dark: #0D0D0F;
    --dark2: #151518;
    --dark3: #1E1E24;
    --dark4: #2A2A32;
    --text: #E8E6DF;
    --text-muted: #8A8880;
    --accent: #4A90D9;
    --green: #5DBE8A;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #1a1508 0%, var(--dark) 50%),
                radial-gradient(ellipse at 80% 100%, #081520 0%, transparent 50%);
    background-color: var(--dark);
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1rem; max-width: 900px;}

/* ── HERO ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 700;
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 50%, #a07830 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.3rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--text-muted);
    font-weight: 300;
    letter-spacing: 0.04em;
}

/* ── CARDS ── */
.card {
    background: var(--dark3);
    border: 1px solid rgba(201,168,76,0.18);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 32px rgba(0,0,0,0.4);
}
.card-gold {
    border-color: rgba(201,168,76,0.5);
    background: linear-gradient(135deg, rgba(201,168,76,0.07) 0%, var(--dark3) 100%);
}

/* ── STEP BADGE ── */
.step-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(201,168,76,0.12);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 50px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--gold);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── PROGRESS ── */
.progress-container {
    display: flex;
    gap: 6px;
    margin-bottom: 2rem;
    align-items: center;
}
.progress-dot {
    width: 32px; height: 4px;
    border-radius: 2px;
    background: var(--dark4);
    transition: background 0.3s;
}
.progress-dot.active { background: var(--gold); }
.progress-dot.done { background: rgba(201,168,76,0.45); }
.progress-label {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-left: 6px;
}

/* ── QUESTION CARD ── */
.question-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 400;
    color: var(--text);
    margin-bottom: 0.25rem;
}
.question-hint {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 1.2rem;
}

/* ── PROFILE BLOCK ── */
.profile-type {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--gold-light);
    margin: 0.2rem 0;
}
.profile-tag {
    display: inline-block;
    background: rgba(201,168,76,0.15);
    color: var(--gold);
    border-radius: 50px;
    padding: 2px 12px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 3px 3px 3px 0;
    border: 1px solid rgba(201,168,76,0.25);
}

/* ── CHAT ── */
.chat-msg-user {
    background: rgba(74,144,217,0.12);
    border: 1px solid rgba(74,144,217,0.25);
    border-radius: 14px 14px 4px 14px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.95rem;
    max-width: 80%;
    margin-left: auto;
    color: #c8dfff;
}
.chat-msg-ai {
    background: var(--dark3);
    border: 1px solid rgba(201,168,76,0.18);
    border-radius: 14px 14px 14px 4px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.95rem;
    max-width: 90%;
    line-height: 1.65;
}
.chat-msg-ai h3 { color: var(--gold-light); font-family: 'Playfair Display', serif; }
.chat-msg-ai strong { color: var(--gold); }
.chat-msg-ai ul { padding-left: 1.2rem; }
.chat-role-user {
    text-align: right;
    font-size: 0.72rem;
    color: var(--accent);
    margin-bottom: 2px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.chat-role-ai {
    font-size: 0.72rem;
    color: var(--gold);
    margin-bottom: 2px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--gold) 0%, #a07830 100%);
    color: #0D0D0F;
    border: none;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.6rem 1.8rem;
    letter-spacing: 0.03em;
    transition: all 0.2s;
    box-shadow: 0 2px 16px rgba(201,168,76,0.25);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 24px rgba(201,168,76,0.4);
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 100%);
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--dark4) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(201,168,76,0.6) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.12) !important;
}

.stSelectbox > div > div {
    background: var(--dark4) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stRadio > div { gap: 0.5rem; }
.stRadio label {
    background: var(--dark3) !important;
    border: 1px solid var(--dark4) !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    color: var(--text) !important;
    cursor: pointer;
    transition: all 0.2s;
}
.stRadio label:hover {
    border-color: rgba(201,168,76,0.4) !important;
}

/* ── DIVIDER ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(201,168,76,0.4), transparent);
    margin: 1.5rem 0;
}

/* ── ROUTE DISPLAY ── */
.route-content {
    line-height: 1.8;
    font-size: 0.97rem;
}
.route-content h2 {
    font-family: 'Playfair Display', serif;
    color: var(--gold-light);
    font-size: 1.5rem;
    margin: 1.5rem 0 0.5rem;
    border-bottom: 1px solid rgba(201,168,76,0.2);
    padding-bottom: 0.3rem;
}
.route-content h3 {
    color: var(--gold);
    font-size: 1.1rem;
    margin: 1rem 0 0.3rem;
}
.route-content strong { color: var(--gold); }
.route-content ul { padding-left: 1.3rem; }
.route-content li { margin-bottom: 0.3rem; }

/* ── SPINNER ── */
.stSpinner > div {
    border-top-color: var(--gold) !important;
}

/* ── API KEY SECTION ── */
.api-note {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "step": "api_key",          # api_key → survey → profile → route → chat
        "api_key": "",
        "answers": {},
        "profile": {},
        "route_text": "",
        "chat_history": [],          # list of {"role": "user"|"assistant", "content": str}
        "current_q": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# QUESTIONS
# ─────────────────────────────────────────────
QUESTIONS = [
    {
        "id": "destination",
        "emoji": "🗺️",
        "title": "Куда мечтаете отправиться?",
        "hint": "Укажите страну, регион или город — конкретно или примерно",
        "type": "text",
        "placeholder": "Например: Япония, побережье Амальфи, Патагония…",
    },
    {
        "id": "duration",
        "emoji": "📅",
        "title": "Сколько дней у вас есть?",
        "hint": "Общая продолжительность поездки",
        "type": "radio",
        "options": ["3–5 дней", "6–10 дней", "11–14 дней", "15–21 день", "Больше трёх недель"],
    },
    {
        "id": "travel_style",
        "emoji": "🎭",
        "title": "Как вы путешествуете?",
        "hint": "Выберите наиболее близкий стиль",
        "type": "radio",
        "options": [
            "Соло — люблю свободу и одиночество",
            "Пара — романтика и близость",
            "Семья с детьми — безопасно и познавательно",
            "Друзья — веселье и приключения",
            "Деловая поездка с возможностью отдохнуть",
        ],
    },
    {
        "id": "vibe",
        "emoji": "✨",
        "title": "Что вас больше всего заряжает?",
        "hint": "Ваш главный источник вдохновения в путешествии",
        "type": "radio",
        "options": [
            "🏛️ История, культура, архитектура",
            "🌿 Природа, тишина, пешие маршруты",
            "🍽️ Гастрономия и местная кухня",
            "🎉 Ночная жизнь, вечеринки, тусовки",
            "🧘 Медитация, ретриты, духовный опыт",
            "🏄 Экстрим, спорт, активный отдых",
        ],
    },
    {
        "id": "budget",
        "emoji": "💰",
        "title": "Ваш бюджет на человека в день?",
        "hint": "Включая жильё, еду и активности",
        "type": "radio",
        "options": [
            "До $50 — бэкпекер-режим",
            "$50–120 — комфортный средний",
            "$120–250 — хороший уровень",
            "$250–500 — бизнес-класс",
            "Более $500 — люкс без ограничений",
        ],
    },
    {
        "id": "accommodation",
        "emoji": "🛏️",
        "title": "Где вы предпочитаете останавливаться?",
        "hint": "Тип жилья, который вам ближе",
        "type": "radio",
        "options": [
            "Хостел / капсульный отель",
            "Уютный b&b или гестхаус",
            "Городской 3-4★ отель",
            "Бутик-отель или дизайн-хостел",
            "5★ или luxury resort",
            "Арендное жильё (Airbnb, апартаменты)",
        ],
    },
    {
        "id": "pace",
        "emoji": "⏱️",
        "title": "Какой ритм поездки вам нравится?",
        "hint": "Как вы распределяете активность и отдых",
        "type": "radio",
        "options": [
            "Плотный — 5–7 точек в день, всё успеть",
            "Умеренный — 2–3 места + время на прогулки",
            "Расслабленный — 1–2 цели, много кафе и созерцания",
            "Импровизация — никакого плана, куда понесёт",
        ],
    },
    {
        "id": "fear",
        "emoji": "⚠️",
        "title": "Что вас раздражает или пугает в поездках?",
        "hint": "Что точно НЕ должно быть в маршруте",
        "type": "text",
        "placeholder": "Например: толпы туристов, долгие переезды, отсутствие Wi-Fi, острая еда…",
    },
    {
        "id": "dream",
        "emoji": "🌠",
        "title": "Опишите идеальный момент поездки",
        "hint": "Одно предложение — что вы хотите почувствовать или сделать",
        "type": "text",
        "placeholder": "Например: встретить закат над морем с бокалом вина…",
    },
]


# ─────────────────────────────────────────────
# DEEPSEEK API CALL
# ─────────────────────────────────────────────
def call_deepseek(messages: list, system_prompt: str = "") -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.session_state.api_key}",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system_prompt}] + messages if system_prompt else messages,
        "max_tokens": 3000,
        "temperature": 0.85,
    }
    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=90,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 401:
            return "❌ Ошибка авторизации: проверьте API-ключ DeepSeek."
        return f"❌ HTTP ошибка {resp.status_code}: {e}"
    except Exception as e:
        return f"❌ Ошибка подключения: {e}"


def build_profile_prompt(answers: dict) -> str:
    return f"""
Ты — опытный психолог-трэвел-консультант. 
Проанализируй ответы путешественника и составь его психологический профиль.

Ответы пользователя:
- Направление: {answers.get('destination', '—')}
- Длительность: {answers.get('duration', '—')}
- Стиль путешествия: {answers.get('travel_style', '—')}
- Главный интерес: {answers.get('vibe', '—')}
- Бюджет в день: {answers.get('budget', '—')}
- Жильё: {answers.get('accommodation', '—')}
- Темп: {answers.get('pace', '—')}
- Что раздражает: {answers.get('fear', '—')}
- Идеальный момент: {answers.get('dream', '—')}

Верни ТОЛЬКО JSON без Markdown-обёртки в формате:
{{
  "traveler_type": "Название типа путешественника (1–3 слова)",
  "emoji": "один emoji символизирующий тип",
  "tagline": "яркий слоган этого типа путешественника (до 12 слов)",
  "motivation": "2–3 предложения о глубинной мотивации",
  "strengths": ["сильная сторона 1", "сильная сторона 2", "сильная сторона 3"],
  "watch_out": "1–2 предложения о чём стоит быть осторожным",
  "personality_tags": ["тег1", "тег2", "тег3", "тег4", "тег5"]
}}
"""


def build_route_prompt(answers: dict, profile: dict) -> str:
    return f"""
Ты — элитный тревел-планировщик с 20 годами опыта. Создай детальный маршрут путешествия.

ПРОФИЛЬ ПУТЕШЕСТВЕННИКА:
Тип: {profile.get('traveler_type', '—')} {profile.get('emoji', '')}
Мотивация: {profile.get('motivation', '—')}

ПАРАМЕТРЫ ПОЕЗДКИ:
- Направление: {answers.get('destination', '—')}
- Длительность: {answers.get('duration', '—')}
- Компания: {answers.get('travel_style', '—')}
- Главный интерес: {answers.get('vibe', '—')}
- Бюджет/день: {answers.get('budget', '—')}
- Жильё: {answers.get('accommodation', '—')}
- Темп: {answers.get('pace', '—')}
- Не нравится: {answers.get('fear', '—')}
- Мечта поездки: {answers.get('dream', '—')}

Составь полный маршрут включая:
1. **Краткий обзор** — почему это направление идеально для этого путешественника
2. **Маршрут по дням** — для каждого дня: утро/день/вечер с конкретными локациями
3. **Топ-5 мест** которые нельзя пропустить (с пояснением почему)
4. **Гастрономический гид** — 3–5 ресторанов/кафе/рынков с описанием
5. **Практические советы** — транспорт, жильё (конкретный район), лайфхаки
6. **Бюджет** — примерная разбивка расходов по категориям
7. **Идеальный момент** — как воплотить мечту путешественника

Пиши живо, вдохновляюще, с конкретными деталями. Используй Markdown для структуры.
"""


# ─────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────
def render_progress(current: int, total: int):
    dots = ""
    for i in range(total):
        if i < current:
            dots += '<div class="progress-dot done"></div>'
        elif i == current:
            dots += '<div class="progress-dot active"></div>'
        else:
            dots += '<div class="progress-dot"></div>'
    st.markdown(
        f'<div class="progress-container">{dots}'
        f'<span class="progress-label">{current + 1} / {total}</span></div>',
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1.5rem;">
        <div class="hero-title">AI Travel Guide</div>
        <div class="hero-sub">Персональный маршрут, созданный по вашей душе</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP: API KEY
# ─────────────────────────────────────────────
def step_api_key():
    render_hero()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="card card-gold">
            <div class="step-badge">🔑 Подключение</div>
            <div class="question-title">Введите API-ключ DeepSeek</div>
            <div class="question-hint">
                Ключ нужен для работы AI. Он хранится только в памяти сессии
                и никуда не передаётся. Получить ключ можно на
                <a href="https://platform.deepseek.com" target="_blank" style="color:var(--gold)">platform.deepseek.com</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        key_input = st.text_input(
            "API Key",
            type="password",
            placeholder="sk-...",
            label_visibility="collapsed",
        )
        st.markdown('<div class="api-note">🔒 Ключ существует только в рамках этой сессии браузера</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Начать путешествие →", use_container_width=True):
            if key_input.strip():
                st.session_state.api_key = key_input.strip()
                st.session_state.step = "survey"
                st.rerun()
            else:
                st.error("Пожалуйста, введите API-ключ.")


# ─────────────────────────────────────────────
# STEP: SURVEY
# ─────────────────────────────────────────────
def step_survey():
    render_hero()
    q_idx = st.session_state.current_q
    q = QUESTIONS[q_idx]

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        render_progress(q_idx, len(QUESTIONS))

        st.markdown(f"""
        <div class="card">
            <div class="step-badge">{q['emoji']} Вопрос {q_idx + 1}</div>
            <div class="question-title">{q['title']}</div>
            <div class="question-hint">{q['hint']}</div>
        </div>
        """, unsafe_allow_html=True)

        answer = None
        if q["type"] == "text":
            answer = st.text_input(
                "answer",
                value=st.session_state.answers.get(q["id"], ""),
                placeholder=q.get("placeholder", ""),
                label_visibility="collapsed",
                key=f"q_{q_idx}_text",
            )
        elif q["type"] == "radio":
            prev = st.session_state.answers.get(q["id"])
            opts = q["options"]
            idx = opts.index(prev) if prev in opts else 0
            answer = st.radio(
                "answer",
                options=opts,
                index=idx,
                label_visibility="collapsed",
                key=f"q_{q_idx}_radio",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        col_back, col_next = st.columns([1, 2])

        with col_back:
            if q_idx > 0:
                if st.button("← Назад", use_container_width=True):
                    st.session_state.current_q -= 1
                    st.rerun()

        with col_next:
            is_last = q_idx == len(QUESTIONS) - 1
            btn_label = "Построить профиль ✨" if is_last else "Далее →"
            if st.button(btn_label, use_container_width=True):
                if answer and str(answer).strip():
                    st.session_state.answers[q["id"]] = answer
                    if is_last:
                        st.session_state.step = "profile"
                        st.session_state.current_q = 0
                    else:
                        st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.warning("Пожалуйста, ответьте на вопрос.")


# ─────────────────────────────────────────────
# STEP: PROFILE
# ─────────────────────────────────────────────
def step_profile():
    render_hero()

    if not st.session_state.profile:
        with st.spinner("🧬 Анализируем ваш психологический профиль…"):
            prompt = build_profile_prompt(st.session_state.answers)
            raw = call_deepseek([{"role": "user", "content": prompt}])
            try:
                clean = raw.strip().strip("```json").strip("```").strip()
                profile = json.loads(clean)
            except Exception:
                profile = {
                    "traveler_type": "Исследователь",
                    "emoji": "🧭",
                    "tagline": "Каждая дорога — это открытие",
                    "motivation": raw[:300],
                    "strengths": ["Любопытство", "Адаптивность", "Открытость"],
                    "watch_out": "Берегите силы и не перегружайте программу.",
                    "personality_tags": ["#curious", "#flexible", "#adventurous"],
                }
        st.session_state.profile = profile
        st.rerun()

    p = st.session_state.profile
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
        <div class="card card-gold">
            <div class="step-badge">🧬 Ваш профиль</div>
            <div style="font-size:3rem; margin-bottom:0.3rem">{p.get('emoji','🌍')}</div>
            <div class="profile-type">{p.get('traveler_type','Путешественник')}</div>
            <div style="color:var(--text-muted); font-style:italic; margin-bottom:1rem">
                «{p.get('tagline','')}»
            </div>
            <div class="gold-divider"></div>
            <p style="line-height:1.7; color:var(--text-muted)">{p.get('motivation','')}</p>
            <div style="margin:0.8rem 0">
                {''.join([f'<span class="profile-tag">{t}</span>' for t in p.get('personality_tags',[])])}
            </div>
            <div class="gold-divider"></div>
            <div style="margin-bottom:0.5rem; font-size:0.85rem; color:var(--gold); font-weight:600">
                💪 Сильные стороны
            </div>
            {''.join([f'<div style="font-size:0.9rem; margin:3px 0; color:var(--text-muted)">• {s}</div>' for s in p.get('strengths',[])])}
            <div style="margin-top:1rem; font-size:0.85rem; color:var(--text-muted)">
                ⚠️ {p.get('watch_out','')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗺️ Сгенерировать маршрут", use_container_width=True):
            st.session_state.step = "route"
            st.rerun()


# ─────────────────────────────────────────────
# STEP: ROUTE
# ─────────────────────────────────────────────
def step_route():
    render_hero()

    if not st.session_state.route_text:
        dest = st.session_state.answers.get("destination", "путешествие")
        with st.spinner(f"✈️ Создаём ваш персональный маршрут в {dest}…"):
            prompt = build_route_prompt(st.session_state.answers, st.session_state.profile)
            route = call_deepseek([{"role": "user", "content": prompt}])
        st.session_state.route_text = route

        # Seed chat history with route context
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": route,
            }
        ]
        st.rerun()

    p = st.session_state.profile
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="step-badge">✈️ Ваш маршрут · {p.get('traveler_type','')} {p.get('emoji','')}</div>
            <div class="route-content">
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.route_text)
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💬 Уточнить и адаптировать маршрут", use_container_width=True):
            st.session_state.step = "chat"
            st.rerun()


# ─────────────────────────────────────────────
# STEP: CHAT
# ─────────────────────────────────────────────
SYSTEM_CHAT = """
Ты — персональный тревел-консультант высокого класса. 
У тебя уже есть полный маршрут путешественника — он указан в истории диалога.
Отвечай конкретно, вдохновляюще, с деталями.
Если просят изменить маршрут — предлагай конкретные правки.
Используй Markdown для структурирования ответов.
Помни психологический профиль путешественника и подстраивай рекомендации под него.
"""

def step_chat():
    render_hero()

    p = st.session_state.profile
    history = st.session_state.chat_history

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="step-badge">💬 Диалог с AI-гидом · {p.get('traveler_type','')} {p.get('emoji','')}</div>
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem">
                Задавайте вопросы, уточняйте детали, просите изменить маршрут
            </div>
        """, unsafe_allow_html=True)

        # Show first message (route) in collapsed form
        if len(history) >= 1 and history[0]["role"] == "assistant":
            with st.expander("📋 Ваш маршрут (свернуть/развернуть)", expanded=False):
                st.markdown(history[0]["content"])

        # Chat messages (skip first route message)
        for msg in history[1:]:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-role-user">Вы</div><div class="chat-msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-role-ai">✦ AI-гид</div><div class="chat-msg-ai">', unsafe_allow_html=True)
                st.markdown(msg["content"])
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Input
        st.markdown("<br>", unsafe_allow_html=True)
        user_input = st.text_area(
            "Ваш вопрос",
            placeholder="Например: Можно заменить день 3 на горный поход? Или: Порекомендуй ресторан с видом на закат…",
            label_visibility="collapsed",
            key="chat_input",
            height=90,
        )

        col_send, col_reset = st.columns([3, 1])
        with col_send:
            if st.button("Отправить →", use_container_width=True):
                if user_input.strip():
                    st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
                    with st.spinner("AI-гид думает…"):
                        # Build messages: system context + full history
                        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                        reply = call_deepseek(messages, system_prompt=SYSTEM_CHAT)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()

        with col_reset:
            if st.button("↩ Маршрут", use_container_width=True):
                st.session_state.step = "route"
                st.rerun()

        # Quick prompts
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.5rem">Быстрые вопросы:</div>', unsafe_allow_html=True)
        quick_cols = st.columns(3)
        quick_prompts = [
            "💡 Альтернативный день",
            "🍽️ Больше ресторанов",
            "💰 Как сэкономить?",
            "🚆 Советы по транспорту",
            "📷 Лучшие фото-точки",
            "🌧️ Что если дождь?",
        ]
        for i, qp in enumerate(quick_prompts):
            with quick_cols[i % 3]:
                if st.button(qp, use_container_width=True, key=f"qp_{i}"):
                    st.session_state.chat_history.append({"role": "user", "content": qp})
                    with st.spinner("AI-гид думает…"):
                        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                        reply = call_deepseek(messages, system_prompt=SYSTEM_CHAT)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()


# ─────────────────────────────────────────────
# SIDEBAR — navigation & reset
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🌍 AI Travel Guide")
        st.markdown("---")
        step = st.session_state.step
        steps_map = {
            "api_key": ("🔑", "API Ключ"),
            "survey": ("📋", "Опрос"),
            "profile": ("🧬", "Профиль"),
            "route": ("🗺️", "Маршрут"),
            "chat": ("💬", "Диалог"),
        }
        for s, (icon, label) in steps_map.items():
            active = "**" if s == step else ""
            st.markdown(f"{icon} {active}{label}{active}")

        st.markdown("---")
        if step != "api_key":
            if st.button("🔄 Начать заново", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                init_state()
                st.rerun()

        if step in ("route", "chat") and st.session_state.profile:
            p = st.session_state.profile
            st.markdown(f"""
            **Ваш тип:**  
            {p.get('emoji','')} {p.get('traveler_type','')}

            *«{p.get('tagline','')}»*
            """)


# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
render_sidebar()

step = st.session_state.step
if step == "api_key":
    step_api_key()
elif step == "survey":
    step_survey()
elif step == "profile":
    step_profile()
elif step == "route":
    step_route()
elif step == "chat":
    step_chat()
