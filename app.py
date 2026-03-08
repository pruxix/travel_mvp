import streamlit as st
import requests
import json
import os

# ════════════════════════════════════════════════════════════════
#  PAGE CONFIG
#  Меняй: title, icon, layout
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="✈️ AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════
#  CSS / ДИЗАЙН
#  Меняй: цвета в :root, шрифты, стили карточек, кнопок
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg:     #0D1B2A;
    --bg2:    #112233;
    --card:   #162840;
    --border: rgba(100,160,220,0.18);
    --teal:   #4ECDC4;
    --gold:   #FFD166;
    --accent: #74B9FF;
    --text:   #E8F4FD;
    --muted:  #8BAABB;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text); background: var(--bg) !important; }
.stApp { background: var(--bg) !important; min-height: 100vh; }
h1,h2,h3,h4 { font-family: 'Cormorant Garamond', serif; }

/* Фоновые свечения */
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(78,205,196,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(116,185,255,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, rgba(255,209,102,0.05) 0%, transparent 40%);
}

/* Hero */
.hero { text-align:center; padding:3.5rem 1rem 2.5rem; }
.hero h1 {
    font-size:3.6rem; font-weight:700; letter-spacing:-1px; margin-bottom:0.6rem;
    background:linear-gradient(135deg, var(--teal), var(--accent), var(--gold));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero p { font-size:1.1rem; color:var(--muted); font-weight:300; }

/* Прогресс шагов */
.step-bar {
    display:flex; justify-content:center; margin:0 auto 2.5rem; max-width:720px; position:relative; z-index:1;
}
.step-bar::before {
    content:''; position:absolute; top:21px; left:10%; width:80%; height:2px;
    background:linear-gradient(90deg, var(--teal), var(--gold)); opacity:.3; z-index:0;
}
.step-item { display:flex; flex-direction:column; align-items:center; gap:8px; flex:1; z-index:1; }
.step-circle {
    width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center;
    font-size:1rem; font-weight:700; border:2px solid transparent; transition:all .3s;
}
.step-circle.active   { background:var(--teal); color:var(--bg); border-color:var(--teal); box-shadow:0 0 18px rgba(78,205,196,.4); }
.step-circle.done     { background:transparent; color:var(--gold); border-color:var(--gold); }
.step-circle.inactive { background:var(--card); color:var(--muted); border-color:var(--border); }
.step-label { font-size:.65rem; font-weight:500; color:var(--muted); text-align:center; max-width:70px; line-height:1.3; text-transform:uppercase; letter-spacing:.04em; }

/* Карточки */
.card {
    background:var(--card); border:1px solid var(--border); border-radius:20px;
    padding:2rem 2.4rem; margin-bottom:1.6rem; box-shadow:0 8px 40px rgba(0,0,0,.3); position:relative; overflow:hidden;
}
.card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg, var(--teal), var(--accent)); opacity:.6; }

/* Значки профиля */
.profile-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:1.2rem 0; }
.profile-badge { background:rgba(78,205,196,.07); border:1px solid rgba(78,205,196,.2); border-radius:14px; padding:14px 16px; text-align:center; }
.badge-label { font-size:.65rem; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }
.badge-value { font-size:1.1rem; font-weight:600; color:var(--teal); margin-top:5px; font-family:'Cormorant Garamond',serif; }

/* Тег */
.tag { display:inline-block; background:rgba(255,209,102,.1); border:1px solid rgba(255,209,102,.3); border-radius:20px; padding:3px 12px; font-size:.78rem; font-weight:500; color:var(--gold); margin:3px; }

/* Маршрут — читабельные цвета */
.route-wrap { line-height:1.85; color:var(--text); }
.route-wrap h2 { color:var(--teal); font-size:1.7rem; margin:1.8rem 0 .6rem; border-bottom:1px solid rgba(78,205,196,.2); padding-bottom:.4rem; }
.route-wrap h3 { color:var(--accent); font-size:1.3rem; margin:1.2rem 0 .4rem; }
.route-wrap h4 { color:var(--gold); font-size:1.05rem; margin:.9rem 0 .3rem; }
.route-wrap p  { color:#C8DFF0; margin-bottom:.6rem; }
.route-wrap ul { padding-left:1.4rem; }
.route-wrap li { color:#C8DFF0; margin-bottom:5px; }
.route-wrap strong { color:var(--text); }
.route-wrap table { width:100%; border-collapse:collapse; margin:1rem 0; }
.route-wrap th { background:rgba(78,205,196,.15); color:var(--teal); padding:8px 12px; text-align:left; font-size:.85rem; }
.route-wrap td { padding:7px 12px; border-bottom:1px solid var(--border); color:#C8DFF0; font-size:.9rem; }

/* Чат */
.chat-msg { margin-bottom:1rem; }
.chat-msg.user { text-align:right; }
.chat-bubble { display:inline-block; max-width:82%; padding:11px 16px; border-radius:18px; font-size:.93rem; line-height:1.55; text-align:left; }
.user .chat-bubble { background:var(--teal); color:var(--bg); border-bottom-right-radius:4px; font-weight:500; }
.assistant .chat-bubble { background:var(--bg2); color:var(--text); border:1px solid var(--border); border-bottom-left-radius:4px; }

/* Кнопки */
.stButton > button {
    background:linear-gradient(135deg, var(--teal), #2EAFA7) !important;
    color:var(--bg) !important; border:none !important; border-radius:12px !important;
    padding:.55rem 1.8rem !important; font-family:'Inter',sans-serif !important;
    font-weight:600 !important; font-size:.9rem !important; transition:all .25s !important;
    box-shadow:0 4px 18px rgba(78,205,196,.25) !important; letter-spacing:.02em !important;
}
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 6px 24px rgba(78,205,196,.4) !important; }

/* Инпуты */
.stRadio label { color:var(--text) !important; }
div[data-testid="stRadio"] > div > label {
    background:var(--bg2) !important; border:1px solid var(--border) !important;
    border-radius:10px !important; padding:8px 14px !important; color:var(--text) !important; transition:border-color .2s !important;
}
div[data-testid="stRadio"] > div > label:hover { border-color:var(--teal) !important; }
.stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
    background:var(--bg2) !important; border:1px solid var(--border) !important;
    border-radius:12px !important; color:var(--text) !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color:var(--teal) !important; box-shadow:0 0 0 2px rgba(78,205,196,.15) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label { color:var(--muted) !important; font-size:.85rem !important; }

/* Прогресс-бар */
.stProgress > div > div { background:linear-gradient(90deg, var(--teal), var(--accent)) !important; border-radius:4px !important; }
.stProgress > div { background:var(--bg2) !important; border-radius:4px !important; }

/* Скролл */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
hr { border-color:var(--border); margin:1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  SESSION STATE
#  Добавляй новые поля здесь при необходимости
# ════════════════════════════════════════════════════════════════
for key, val in {
    "step": 0,          # 0=город, 1=опрос, 2=профиль, 3=маршрут, 4=чат
    "city": "",
    "answers": {},
    "profile": None,
    "route": None,
    "chat_history": [],
    "q_index": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ════════════════════════════════════════════════════════════════
#  ВОПРОСЫ ОПРОСА
#  Добавляй/убирай вопросы, меняй варианты ответов
# ════════════════════════════════════════════════════════════════
QUESTIONS = [
    {"id": "purpose",       "text": "Какова главная цель поездки?",           "type": "radio",  "emoji": "🎯",
     "options": ["Отдых и релаксация", "Приключения и активный туризм", "Культура и история", "Гастрономия и шопинг", "Цифровой номад / работа"]},
    {"id": "travel_style",  "text": "Как вы путешествуете?",                  "type": "radio",  "emoji": "👥",
     "options": ["Соло", "С партнёром", "С семьёй (дети)", "С друзьями"]},
    {"id": "duration",      "text": "Сколько дней займёт поездка?",           "type": "radio",  "emoji": "📅",
     "options": ["2–3 дня (уикенд)", "4–7 дней", "8–14 дней", "Более 2 недель"]},
    {"id": "budget",        "text": "Бюджет на человека (включая перелёт)?",  "type": "radio",  "emoji": "💰",
     "options": ["До $500", "$500–1500", "$1500–3000", "Свыше $3000", "Гибкий / открытый"]},
    {"id": "accommodation", "text": "Предпочтительный тип жилья?",            "type": "radio",  "emoji": "🏨",
     "options": ["Хостел / бюджет", "3★ отель", "4–5★ отель", "Апартаменты / Airbnb", "Бутик-отель"]},
    {"id": "pace",          "text": "Темп путешествия?",                      "type": "radio",  "emoji": "⏱️",
     "options": ["Медленный (1–2 места глубоко)", "Средний (баланс)", "Быстрый (максимум локаций)"]},
    {"id": "interests",     "text": "Что привлекает больше всего?",           "type": "text",   "emoji": "❤️",
     "placeholder": "Природа, музеи, уличная еда, архитектура, пляжи, хайкинг..."},
]

# ════════════════════════════════════════════════════════════════
#  ПОПУЛЯРНЫЕ ГОРОДА
#  Меняй список по своему усмотрению
# ════════════════════════════════════════════════════════════════
POPULAR_CITIES = [
    ("🗼", "Париж"), ("🏯", "Токио"), ("🗽", "Нью-Йорк"), ("🕌", "Стамбул"),
    ("🌴", "Бали"),  ("🏛️", "Рим"),   ("🐉", "Барселона"), ("🎭", "Прага"),
    ("🌃", "Дубай"), ("🌸", "Бангкок"), ("🦁", "Кейптаун"), ("🏔️", "Алматы"),
]

# ════════════════════════════════════════════════════════════════
#  API НАСТРОЙКИ — MISTRAL
#  Меняй: ключ, модель
# ════════════════════════════════════════════════════════════════
MISTRAL_API_KEY = "U4Ttbskkzv9xcOl9RQh13AfjsN7kQ49E"
MISTRAL_URL     = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL   = "mistral-large-latest"

# ════════════════════════════════════════════════════════════════
#  ВЫЗОВ LLM
#  max_tokens увеличен до 4096 чтобы маршрут не обрывался
# ════════════════════════════════════════════════════════════════
def call_llm(system_prompt, user_message, history=None, stream=False, max_tokens=4096):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    payload = {"model": MISTRAL_MODEL, "max_tokens": max_tokens, "messages": messages, "stream": stream}

    if stream:
        # Стриминг: отдаём чанки по мере поступления
        with requests.post(MISTRAL_URL, headers=headers, json=payload, stream=True, timeout=180) as resp:
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
                            obj   = json.loads(data)
                            delta = obj["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            pass
    else:
        # Обычный запрос
        resp = requests.post(MISTRAL_URL, headers=headers, json=payload, timeout=180)
        if not resp.ok:
            st.error(f"Mistral API error {resp.status_code}: {resp.text}")
            return ""
        return resp.json()["choices"][0]["message"]["content"]


def stream_llm(system_prompt, user_message, history=None):
    return call_llm(system_prompt, user_message, history, stream=True, max_tokens=4096)

# ════════════════════════════════════════════════════════════════
#  ПРОМПТЫ
#  Меняй тексты и структуру промптов
# ════════════════════════════════════════════════════════════════
def build_profile_prompt(answers, city):
    return f"""Ты — психолог-путешествий. На основе ответов пользователя создай профиль.

Город: {city}
Ответы:
{json.dumps(answers, ensure_ascii=False, indent=2)}

Верни ТОЛЬКО валидный JSON (без markdown, без пояснений):
{{"traveler_type":"тип (1-3 слова)","archetype":"архетип","motivation":"мотивация (1 предложение)","style":"стиль (1-2 предложения)","strengths":["сила 1","сила 2","сила 3"],"challenges":["сложность"],"perfect_destination_type":"идеальный тип"}}"""


def build_route_prompt(answers, profile, city):
    duration = answers.get("duration", "7 дней")
    return f"""Ты — элитный тревел-консьерж. Создай ПОЛНЫЙ и ПОДРОБНЫЙ маршрут для: {city}.

Профиль путешественника: {json.dumps(profile, ensure_ascii=False)}
Предпочтения: {json.dumps(answers, ensure_ascii=False)}
Длительность: {duration}

КРИТИЧЕСКИ ВАЖНО: пиши маршрут ПОЛНОСТЬЮ, не останавливайся на середине, доведи до конца все разделы.

Формат Markdown:

## 🗺️ Направление и концепция
2-3 предложения о духе поездки.

## 📅 Маршрут по дням
Для КАЖДОГО дня (от 1 до последнего):
### День N — Название дня
**🌅 Утро:** конкретные активности с названиями мест
**☀️ День:** конкретные активности с названиями мест
**🌙 Вечер:** конкретные активности с названиями мест

## 📍 Топ-7 локаций
Список с кратким описанием каждой.

## 🍜 Гастрономия (5 мест)
Конкретные рестораны/рынки с описанием блюд.

## 💰 Бюджет
| Категория | Стоимость |
|---|---|
| Перелёт | ... |
| Жильё | ... |
| Питание | ... |
| Транспорт | ... |
| Развлечения | ... |
| **Итого** | **...** |

## 💡 Инсайдерские советы
4 практических совета для этого города."""

# ════════════════════════════════════════════════════════════════
#  UI: ПРОГРЕСС-БАР
# ════════════════════════════════════════════════════════════════
def render_step_bar(current):
    steps = [("🏙️","Город"),("🧾","Опрос"),("🧬","Профиль"),("💡","Маршрут"),("💬","Диалог")]
    circles = []
    for i,(icon,label) in enumerate(steps):
        cls = "done" if i < current else ("active" if i == current else "inactive")
        circles.append(f'<div class="step-item"><div class="step-circle {cls}">{icon}</div><div class="step-label">{label}</div></div>')
    st.markdown(f'<div class="step-bar">{"".join(circles)}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  ШАГ 0: ВЫБОР ГОРОДА
# ════════════════════════════════════════════════════════════════
def render_city_select():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🏙️ Куда летим?")
    st.markdown(
        "<p style='color:#6b7280;margin-bottom:1.4rem'>Выберите из популярных направлений или введите свой город</p>",
        unsafe_allow_html=True
    )

    # создаём кнопки для городов в виде облака
    cols_per_row = 5  # 5 кнопок в строке
    current = st.session_state.get("city", "")
    
    for i in range(0, len(POPULAR_CITIES), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, (flag, name) in enumerate(POPULAR_CITIES[i:i+cols_per_row]):
            with cols[j]:
                btn_text = f"{flag} {name}"
                if st.button(btn_text):
                    st.session_state.city = name
                    st.session_state.step = 2  # следующий шаг
                    st.rerun()

    # текстовый ввод для произвольного города
    st.markdown(
        "<p style='color:#6b7280;font-size:.85rem;margin-top:1rem'>Или введите другой город:</p>",
        unsafe_allow_html=True
    )
    custom = st.text_input("", placeholder="Лиссабон, Сеул, Медельин, Тбилиси...", label_visibility="collapsed")
    
    # финальный город
    final_city = custom.strip() if custom.strip() else current
    if final_city:
        st.session_state.city = final_city

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Продолжить →", type="primary"):
        if final_city:
            st.session_state.step = 1  # переходим к следующему шагу
            st.rerun()
        else:
            st.warning("Выберите город или введите свой")

# ════════════════════════════════════════════════════════════════
#  ШАГ 1: ОПРОС
# ════════════════════════════════════════════════════════════════
def render_survey():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    city = st.session_state.city
    st.markdown(f"<p style='color:var(--teal);font-size:.88rem;margin-bottom:.5rem'>✈️ Направление: <b>{city}</b></p>", unsafe_allow_html=True)

    q_idx = st.session_state.q_index
    total = len(QUESTIONS)
    st.markdown(f"<p style='color:var(--muted);font-size:.82rem'>Вопрос {q_idx+1} из {total}</p>", unsafe_allow_html=True)
    st.progress(q_idx / total)

    q = QUESTIONS[q_idx]
    st.markdown(f"### {q['emoji']} {q['text']}")

    key = f"ans_{q['id']}"
    if q["type"] == "radio":
        cur = st.session_state.answers.get(q["id"], q["options"][0])
        idx = q["options"].index(cur) if cur in q["options"] else 0
        val = st.radio("", q["options"], index=idx, key=key, label_visibility="collapsed")
    else:
        cur = st.session_state.answers.get(q["id"], "")
        val = st.text_input("", value=cur, placeholder=q.get("placeholder",""), key=key, label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

    col1, _, col3 = st.columns([1, 3, 1])
    with col1:
        lbl = "← Город" if q_idx == 0 else "← Назад"
        if st.button(lbl):
            if q_idx == 0:
                st.session_state.step = 0
            else:
                st.session_state.q_index -= 1
            st.rerun()
    with col3:
        lbl2 = "Далее →" if q_idx < total - 1 else "Завершить ✓"
        if st.button(lbl2, type="primary"):
            st.session_state.answers[q["id"]] = val
            if q_idx < total - 1:
                st.session_state.q_index += 1
            else:
                st.session_state.step = 2
            st.rerun()

# ════════════════════════════════════════════════════════════════
#  ШАГ 2: ПСИХОЛОГИЧЕСКИЙ ПРОФИЛЬ
# ════════════════════════════════════════════════════════════════
def render_profile():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🧬 Ваш профиль путешественника")

    if st.session_state.profile is None:
        with st.spinner("Анализируем ваши предпочтения..."):
            prompt = build_profile_prompt(st.session_state.answers, st.session_state.city)
            try:
                raw = call_llm(
                    "Отвечай ТОЛЬКО валидным JSON без markdown и без пояснений.",
                    prompt, stream=False, max_tokens=500,
                )
                raw = raw.replace("```json","").replace("```","").strip()
                st.session_state.profile = json.loads(raw)
            except Exception:
                st.session_state.profile = {
                    "traveler_type": "Любознательный исследователь", "archetype": "Открытый путешественник",
                    "motivation": "Познавать мир и получать новые впечатления",
                    "style": "Гибкий и открытый к неожиданностям",
                    "strengths": ["Открытость","Любопытство","Адаптивность"],
                    "challenges": ["Сложно остановиться на одном месте"],
                    "perfect_destination_type": "Разнообразные культурные направления",
                }

    p = st.session_state.profile
    st.markdown(f"""
    <div class="profile-grid">
      <div class="profile-badge"><div class="badge-label">Тип</div><div class="badge-value">{p.get('traveler_type','—')}</div></div>
      <div class="profile-badge"><div class="badge-label">Архетип</div><div class="badge-value">{p.get('archetype','—')}</div></div>
      <div class="profile-badge"><div class="badge-label">Идеальный тип</div><div class="badge-value">{p.get('perfect_destination_type','—')[:35]}</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"**🎯 Мотивация:** {p.get('motivation','')}")
    st.markdown(f"**🧭 Стиль:** {p.get('style','')}")

    if p.get("strengths"):
        st.markdown("**✨ Сильные стороны:**")
        for s in p["strengths"]:
            st.markdown(f'<span class="tag">✓ {s}</span>', unsafe_allow_html=True)

    if p.get("challenges"):
        ch = p["challenges"]
        st.markdown(f"\n**⚠️ На заметку:** {ch if isinstance(ch, str) else ', '.join(ch)}")

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("← Назад"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("💡 Сгенерировать маршрут →", type="primary"):
            st.session_state.step = 3
            st.rerun()

# ════════════════════════════════════════════════════════════════
#  ШАГ 3: МАРШРУТ
#  Стриминг + увеличенный max_tokens = маршрут генерируется полностью
# ════════════════════════════════════════════════════════════════
def render_route():
    city = st.session_state.city
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"## 💡 Маршрут по {city}")

    if st.session_state.route is None:
        prompt = build_route_prompt(st.session_state.answers, st.session_state.profile, city)
        result = ""
        placeholder = st.empty()
        for chunk in stream_llm(
            "Ты — лучший тревел-консьерж мира. Пиши маршрут ПОЛНОСТЬЮ до последней строки, никогда не обрывай текст.",
            prompt,
        ):
            result += chunk
            placeholder.markdown(f'<div class="route-wrap">{result}▌</div>', unsafe_allow_html=True)
        placeholder.markdown(f'<div class="route-wrap">{result}</div>', unsafe_allow_html=True)
        st.session_state.route = result
    else:
        st.markdown(f'<div class="route-wrap">{st.session_state.route}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("← Назад"):
            st.session_state.route = None
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("💬 Уточнить маршрут →", type="primary"):
            st.session_state.chat_history = [{"role":"assistant","content":f"Маршрут по {city} готов! 🎉 Могу адаптировать его — изменить дни, добавить рестораны, скорректировать бюджет. Что уточним?"}]
            st.session_state.step = 4
            st.rerun()

# ════════════════════════════════════════════════════════════════
#  ШАГ 4: ЧАТ — УТОЧНЕНИЕ МАРШРУТА
# ════════════════════════════════════════════════════════════════
def render_chat():
    city = st.session_state.city
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"## 💬 Уточнение — {city}")

        for msg in st.session_state.chat_history:
            role_cls = "user" if msg["role"] == "user" else "assistant"
            icon = "🧳" if msg["role"] == "assistant" else "👤"
            st.markdown(f'<div class="chat-msg {role_cls}"><div class="chat-bubble">{icon} {msg["content"]}</div></div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        user_input = st.text_input("", placeholder="Добавь рестораны / измени день 3 / сколько стоит виза...", key="chat_input", label_visibility="collapsed")

        col_a, col_b = st.columns([2, 1])
        with col_a:
            if st.button("Отправить →", type="primary") and user_input.strip():
                st.session_state.chat_history.append({"role":"user","content":user_input})
                system = f"""Ты — тревел-консьерж для поездки в {city}.
Маршрут: {st.session_state.route}
Профиль: {json.dumps(st.session_state.profile, ensure_ascii=False)}
Отвечай конкретно и по делу."""
                history_api = [m for m in st.session_state.chat_history[:-1] if m["role"] in ("user","assistant")]
                resp_text = ""
                with st.spinner(""):
                    for chunk in stream_llm(system, user_input, history_api):
                        resp_text += chunk
                st.session_state.chat_history.append({"role":"assistant","content":resp_text})
                st.rerun()
        with col_b:
            if st.button("← К маршруту"):
                st.session_state.step = 3
                st.rerun()

    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### 📋 {city}")
        if st.session_state.route:
            preview = st.session_state.route[:1500]
            if len(st.session_state.route) > 1500:
                preview += "\n\n*... полный маршрут ←*"
            st.markdown(f'<div class="route-wrap" style="font-size:.83rem">{preview}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("🔄 Начать заново"):
            for k in ["step","city","answers","profile","route","chat_history","q_index"]:
                del st.session_state[k]
            st.rerun()

# ════════════════════════════════════════════════════════════════
#  ГЛАВНАЯ ТОЧКА ВХОДА
#  Меняй: заголовок и подзаголовок hero
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>✈️ TripPersona AI</h1>
  <p>AI-ассистент по планированию путешествий под ваши потребности и настроение</p>
</div>
""", unsafe_allow_html=True)

render_step_bar(st.session_state.step)

if   st.session_state.step == 0: render_city_select()
elif st.session_state.step == 1: render_survey()
elif st.session_state.step == 2: render_profile()
elif st.session_state.step == 3: render_route()
elif st.session_state.step == 4: render_chat()
