import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ------------------------------------------------
# STYLE (фикс цвета текста)
# ------------------------------------------------

st.markdown("""
<style>

.stApp{
background-color:#f4f6fb;
color:#111827;
}

/* основной контейнер */

.block-container{
max-width:900px;
margin:auto;
}

/* текст */

h1,h2,h3,h4,h5,p,label,span,div{
color:#111827 !important;
}

/* radio / select */

.stRadio label,
.stSelectbox label{
color:#111827 !important;
}

/* input */

input, textarea{
color:#111827 !important;
background:white !important;
}

/* dropdown */

.stSelectbox div{
color:#111827 !important;
}

/* radio options */

.stRadio div{
color:#111827 !important;
}

/* header card */

.header-card{
background:white;
padding:40px;
border-radius:16px;
box-shadow:0 10px 25px rgba(0,0,0,0.08);
text-align:center;
margin-bottom:30px;
}

.header-title{
font-size:34px;
font-weight:700;
color:#111827;
}

.header-sub{
color:#4b5563;
}

/* city buttons */

.stButton button{
background:white;
color:#111827;
border:1px solid #d1d5db;
border-radius:20px;
padding:8px 16px;
}

.stButton button:hover{
background:#6366f1;
color:white;
}

/* place cards */

.place-card{
background:white;
padding:20px;
border-radius:14px;
box-shadow:0 4px 14px rgba(0,0,0,0.08);
margin-bottom:15px;
}

.place-title{
font-size:18px;
font-weight:600;
}

.place-desc{
color:#374151;
}

/* timeline */

.timeline{
border-left:3px solid #6366f1;
padding-left:15px;
}

.timeline-step{
margin-bottom:10px;
color:#111827;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SESSION
# ------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "route" not in st.session_state:
    st.session_state.route = None

# ------------------------------------------------
# CITIES
# ------------------------------------------------

cities = [
"Москва","Санкт-Петербург","Казань","Сочи","Калининград",
"Владивосток","Екатеринбург","Новосибирск","Нижний Новгород",
"Самара","Краснодар","Ростов-на-Дону","Иркутск","Мурманск",
"Ярославль","Суздаль","Владимир","Тула","Кострома","Псков",
"Великий Новгород","Астрахань","Уфа","Челябинск","Пермь",
"Томск","Красноярск","Архангельск","Калуга","Смоленск"
]

# ------------------------------------------------
# PLACES
# ------------------------------------------------

places = [

{"name":"Главная площадь","desc":"Исторический центр города","time":40,"lat":55.751,"lon":37.618,"icon":"🏛"},
{"name":"Городской парк","desc":"Популярное место для прогулок","time":90,"lat":55.760,"lon":37.620,"icon":"🌳"},
{"name":"Главный музей","desc":"Крупнейший музей города","time":120,"lat":55.752,"lon":37.617,"icon":"🖼"},
{"name":"Пешеходная улица","desc":"Улица с кафе и ресторанами","time":60,"lat":55.750,"lon":37.615,"icon":"☕"},
{"name":"Смотровая площадка","desc":"Лучший вид на город","time":30,"lat":55.749,"lon":37.622,"icon":"📸"},
{"name":"Фудмаркет","desc":"Место с местной кухней","time":70,"lat":55.748,"lon":37.621,"icon":"🍜"}

]

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("""
<div class="header-card">
<div class="header-title">🌍 Travel Planner</div>
<div class="header-sub">Создайте маршрут путешествия за 30 секунд</div>
</div>
""", unsafe_allow_html=True)

st.progress(st.session_state.step/3)

# ------------------------------------------------
# STEP 1
# ------------------------------------------------

if st.session_state.step == 1:

    st.subheader("🏙 Выберите город")

    cols = st.columns(5)

    for i,city in enumerate(cities):

        with cols[i % 5]:

            if st.button(city):

                st.session_state.city = city
                st.session_state.step = 2
                st.rerun()

    custom_city = st.text_input("Или введите свой город")

    if st.button("Продолжить"):

        if custom_city:

            st.session_state.city = custom_city
            st.session_state.step = 2
            st.rerun()

# ------------------------------------------------
# STEP 2
# ------------------------------------------------

elif st.session_state.step == 2:

    st.subheader("🧭 Расскажите о поездке")

    pace = st.radio(
        "Темп отдыха",
        ["Активный","Размеренный","Смешанный"]
    )

    interest = st.selectbox(
        "Что интереснее",
        [
            "История и архитектура",
            "Еда",
            "Природа",
            "Музеи",
            "Ночная жизнь"
        ]
    )

    if st.button("Построить маршрут"):

        st.session_state.route = random.sample(places,5)
        st.session_state.step = 3
        st.rerun()

# ------------------------------------------------
# STEP 3
# ------------------------------------------------

elif st.session_state.step == 3:

    st.subheader(f"📍 Маршрут по городу {st.session_state.city}")

    route = st.session_state.route

    for p in route:

        st.markdown(f"""
        <div class="place-card">
        <div class="place-title">{p["icon"]} {p["name"]}</div>
        <div class="place-desc">{p["desc"]}</div>
        ⏱ {p["time"]} минут
        </div>
        """, unsafe_allow_html=True)

    df = pd.DataFrame(route)

    st.subheader("📅 План дня")

    time = 9

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    for p in route:

        st.markdown(
        f'<div class="timeline-step">{time}:00 — {p["name"]}</div>',
        unsafe_allow_html=True
        )

        time += 1

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Новый маршрут"):

        st.session_state.step = 1
        st.session_state.route = None
        st.rerun()
