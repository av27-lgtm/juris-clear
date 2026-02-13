import streamlit as st

# 1. КОНФИГУРАЦИЯ И КУРСЫ ВАЛЮТ (Примерные на сегодня)
USD_TO_AMD = 400  # 1$ = 400 драм
USD_TO_RUB = 90   # 1$ = 90 руб

# 2. СЛОВАРЬ (Теперь со всеми данными и валютами)
translations = {
    "English": {
        "cur": "$", "rate": 1, "lang_code": "EN",
        "title": "⚖️ JurisClear AI",
        "subtitle": "Next-Gen Legal Document Audit",
        "one_time": "Single Audit", "pro": "Unlimited Pro",
        "price_9": "9", "price_29": "29",
        "buy": "Get Started", "upload": "Upload PDF contract",
        "demo_tab": "📝 Sample Report", "main_tab": "🚀 Analysis",
        "demo_content": "🔴 **Critical Risk:** Clause 4.2 allows price increases without notice.\n\n💡 **Advice:** Negotiate a 30-day notice period.",
        "risk_wait": "Waiting for document...",
        "mobile_tip": "Best viewed in portrait mode on mobile."
    },
    "Русский": {
        "cur": "₽", "rate": USD_TO_RUB, "lang_code": "RU",
        "title": "⚖️ JurisClear AI",
        "subtitle": "Юридический аудит нового поколения",
        "one_time": "Разовый аудит", "pro": "Безлимит Pro",
        "price_9": str(9 * USD_TO_RUB), "price_29": str(29 * USD_TO_RUB),
        "buy": "Купить доступ", "upload": "Загрузите PDF договор",
        "demo_tab": "📝 Пример отчета", "main_tab": "🚀 Анализ",
        "demo_content": "🔴 **Критический риск:** Пункт 4.2 позволяет повышать цену без уведомления.\n\n💡 **Совет:** Согласуйте уведомление за 30 дней.",
        "risk_wait": "Ожидание документа...",
        "mobile_tip": "Рекомендуется вертикальный режим на телефоне."
    },
    "Հայերեն": {
        "cur": "֏", "rate": USD_TO_AMD, "lang_code": "AM",
        "title": "⚖️ JurisClear AI",
        "subtitle": "Իրավաբանական աուդիտի նոր սերունդ",
        "one_time": "Մեկանգամյա ստուգում", "pro": "Անսահմանափակ Pro",
        "price_9": str(9 * USD_TO_AMD), "price_29": str(29 * USD_TO_AMD),
        "buy": "Գնել", "upload": "Վերբեռնել PDF պայմանագիրը",
        "demo_tab": "📝 Օրինակ", "main_tab": "🚀 Վերլուծություն",
        "demo_content": "🔴 **Կրիտիկական ռիսկ:** 4.2 կետը թույլ է տալիս բարձրացնել գինը առանց ծանուցման:\n\n💡 **Խորհուրդ.** Պահանջեք 30-օրյա ծանուցման ժամկետ:",
        "risk_wait": "Սպասում ենք փաստաթղթին...",
        "mobile_tip": "Հեռախոսով օգտվելիս խորհուրդ է տրվում ուղղահայաց դիրքը:"
    }
}

st.set_page_config(page_title="JurisClear AI", page_icon="⚖️", layout="wide")

# 3. ШАПКА: ЛОГОТИП И ВЫБОР ЯЗЫКА
head_left, head_right = st.columns([3, 1])

with head_right:
    lang_choice = st.selectbox("", ["Русский", "English", "Հայերեն"], label_visibility="collapsed")
    t = translations[lang_choice]

with head_left:
    st.markdown(f"# {t['title']}")
    st.markdown(f"*{t['subtitle']}*")

st.divider()

# 4. ТАРИФЫ (Адаптивные колонки)
col1, col2 = st.columns(2)

with col1:
    st.info(f"### {t['one_time']}\n## {t['price_9']} {t['cur']}")
    st.button(t['buy'], key="btn9", use_container_width=True)

with col2:
    st.success(f"### {t['pro']}\n## {t['price_29']} {t['cur']} / mo")
    st.button(t['buy'], key="btn29", use_container_width=True)

st.write("---")

# 5. ОСНОВНОЙ ФУНКЦИОНАЛ
tab_main, tab_demo = st.tabs([t['main_tab'], t['demo_tab']])

with tab_main:
    uploaded_file = st.file_uploader(t['upload'], type="pdf")
    if uploaded_file:
        st.toast("File uploaded!")
        st.warning("🔒 Payment required to start AI engine.")
    else:
        st.write(f"ℹ️ {t['risk_wait']}")

with tab_demo:
    st.markdown(f"### {t['demo_tab']}")
    st.write(t['demo_content'])

# 6. ФУТЕР ДЛЯ МОБИЛЬНЫХ
st.divider()
st.caption(f"JurisClear AI © 2026 | {t['mobile_tip']}")
