import streamlit as st

# 1. СЛОВАРЬ ПЕРЕВОДОВ
translations = {
    "Русский": {
        "title": "JurisClear AI",
        "subtitle": "Умный аудит юридических рисков",
        "select_plan": "Выберите тарифный план:",
        "one_time": "📄 Разовый аудит",
        "pro": "👑 Безлимит (Pro)",
        "buy": "Купить доступ",
        "upload": "Загрузите договор в PDF",
        "demo_tab": "📝 Пример отчета",
        "main_tab": "🚀 Анализ",
        "free_advice": "💡 Совет: Всегда проверяйте пункт о 'форс-мажоре' и 'порядке расторжения'.",
        "risk_score": "Оценка риска: 7/10 (Требуется анализ)",
        "bait_text": "Хотите узнать, почему оценка риска высокая? Оплатите полный отчет."
    },
    "English": {
        "title": "JurisClear AI",
        "subtitle": "Smart Legal Risk Audit",
        "select_plan": "Select your plan:",
        "one_time": "📄 Single Audit",
        "pro": "👑 Unlimited (Pro)",
        "buy": "Buy Access",
        "upload": "Upload contract (PDF)",
        "demo_tab": "📝 Sample Report",
        "main_tab": "🚀 Analysis",
        "free_advice": "💡 Tip: Always check 'force majeure' and 'termination' clauses.",
        "risk_score": "Risk Score: 7/10 (Action Required)",
        "bait_text": "Want to know why the risk score is high? Get the full report."
    },
    "Հայերեն": {
        "title": "JurisClear AI",
        "subtitle": "Իրավաբանական ռիսկերի խելացի աուդիտ",
        "select_plan": "Ընտրեք սակագինը.",
        "one_time": "📄 Մեկանգամյա ստուգում",
        "pro": "👑 Անսահմանափակ (Pro)",
        "buy": "Գնել",
        "upload": "Վերբեռնել PDF պայմանագիրը",
        "demo_tab": "📝 Օրինակ",
        "main_tab": "🚀 Վերլուծություն",
        "free_advice": "💡 Խորհուրդ. Միշտ ստուգեք 'ֆորս մաժորի' և 'լուծարման կարգի' կետերը:",
        "risk_score": "Ռիսկի գնահատականը՝ 7/10",
        "bait_text": "Ցանկանու՞մ եք իմանալ, թե ինչու է ռիսկը բարձր: Գնեք ամբողջական հաշվետվությունը:"
    }
}

# Настройка страницы
st.set_page_config(page_title="JurisClear AI", page_icon="⚖️", layout="wide")

# 2. ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКА
lang = st.sidebar.selectbox("🌐 Language / Язык / Լեզու", ["Русский", "English", "Հայերեն"])
t = translations[lang]

# Твои ссылки
link_9usd = "ТВОЯ_ССЫЛКА"
link_29usd = "ТВОЯ_ССЫЛКА"

# Интерфейс
st.markdown(f"<h1 style='text-align: center;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>{t['subtitle']}</p>", unsafe_allow_html=True)

st.write("---")

# Секция советов (Бесплатная ценность)
st.info(t['free_advice'])

col1, col2 = st.columns([1, 1.2])

with col1:
    st.write(f"### {t['select_plan']}")
    st.info(f"{t['one_time']}\n\n**$9**")
    st.link_button(t['buy'], link_9usd, use_container_width=True)
    
    st.success(f"{t['pro']}\n\n**$29/мес**")
    st.link_button(t['buy'], link_29usd, use_container_width=True)

with col2:
    tab_a, tab_b = st.tabs([t['main_tab'], t['demo_tab']])
    with tab_a:
        file = st.file_uploader(t['upload'], type="pdf")
        if file:
            st.write(f"### {t['risk_score']}")
            st.warning(t['bait_text'])
    with tab_b:
        st.write("Пример отчета скоро появится здесь...")

# Дополнительная секция "База знаний"
with st.expander("❓ Часто задаваемые вопросы (FAQ)"):
    if lang == "Русский":
        st.write("1. Это заменяет юриста? - Нет, но это экономит время на базовую проверку.")
        st.write("2. Мои данные в безопасности? - Да, мы не храним ваши файлы после анализа.")
    elif lang == "English":
        st.write("1. Does it replace a lawyer? - No, but it saves time on basic checks.")
        st.write("2. Is my data safe? - Yes, we don't store your files after analysis.")
    else:
        st.write("1. Արդյո՞ք սա փոխարինում է իրավաբանին: - Ոչ, բայց այն խնայում է ժամանակը:")
