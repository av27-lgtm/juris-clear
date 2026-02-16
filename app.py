import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

# --- 1. КОНФИГУРАЦИЯ СТРАНИЦЫ ---
st.set_page_config(
    page_title="JurisClear AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. УДАЛЕНИЕ БРЕНДИНГА STREAMLIT (CSS) ---
# Этот блок полностью скрывает хедер, футер и меню для профессионального вида
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stHeader"] {display: none;}
            .stApp [data-testid="stToolbar"] {display: none;}
            /* Убираем лишние отступы сверху */
            .block-container {padding-top: 2rem; padding-bottom: 2rem;}
            /* Стиль кнопок */
            .stButton>button {width: 100%; border-radius: 8px;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. НАСТРОЙКИ API И ССЫЛОК ---
# Убедись, что ключ вставлен в Settings -> Secrets в Streamlit Cloud
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("Критическая ошибка: OpenAI API Key не найден.")

# Вставь свои реальные ссылки LemonSqueezy сюда
LINK_9USD = "https://jurisclear.lemonsqueezy.com/checkout/buy/..." 
LINK_29USD = "https://jurisclear.lemonsqueezy.com/checkout/buy/..."

# --- 4. ЛОГИКА ИИ ---
def get_ai_analysis(text, lang):
    prompts = {
        "Русский": "Ты профессиональный юрист. Проанализируй текст договора. Найди 3 главных юридических риска и дай оценку безопасности от 1 до 10. Отвечай на русском.",
        "English": "You are a professional lawyer. Analyze the contract text. Find 3 main risks and give a safety score 1-10. Answer in English.",
        "Հայերեն": "Դուք պրոֆեսիոնալ իրավաբան եք: Վերլուծեք պայմանագիրը: Գտեք 3 հիմնական ռիսկերը և տվեք անվտանգության գնահատական 1-ից 10-ը: Պատասխանեք հայերեն:"
    }
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional legal auditor."},
                {"role": "user", "content": f"{prompts[lang]}\n\n{text[:4000]}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- 5. СЛОВАРЬ ПЕРЕВОДОВ ---
translations = {
    "English": {
        "cur": "$", "mo": "/ mo", "subtitle": "Professional Legal Document Audit",
        "one_time": "Single Audit", "pro": "Unlimited Pro", "price_9": "9", "price_29": "29",
        "buy": "Get Started", "upload": "Upload PDF contract", "demo_tab": "📝 Sample Report",
        "main_tab": "🚀 AI Analysis", "risk_label": "Legal Risk Assessment:",
        "btn_run": "Start Analysis", "wait_msg": "Please upload a document...",
        "pay_to_unlock": "🔒 Pay {price} {cur} to unlock full legal report.",
        "demo_content": "🔴 **Critical Risk:** Price changes allowed without notice.\n\n🟠 **Medium Risk:** Ambiguous termination terms.\n\n✅ **Verdict:** High risk. Seek legal counsel before signing."
    },
    "Русский": {
        "cur": "$", "mo": "/ мес.", "subtitle": "Профессиональный юридический аудит документов",
        "one_time": "Разовый аудит", "pro": "Безлимит Pro", "price_9": "9", "price_29": "29",
        "buy": "Купить доступ", "upload": "Загрузите PDF договор", "demo_tab": "📝 Пример отчета",
        "main_tab": "🚀 ИИ Анализ", "risk_label": "Оценка юридического риска:",
        "btn_run": "Запустить анализ", "wait_msg": "Загрузите документ для начала...",
        "pay_to_unlock": "🔒 Оплатите {price} {cur}, чтобы открыть полный отчет.",
        "demo_content": "🔴 **Критический риск:** Изменение цены без уведомления.\n\n🟠 **Средний риск:** Размытые условия расторжения.\n\n✅ **Итог:** Высокий риск. Не подписывать без правок."
    },
    "Հայերեն": {
        "cur": "$", "mo": "/ ամիս", "subtitle": "Փաստաթղթերի մասնագիտական իրավական աուդիտ",
        "one_time": "Մեկանգամյա ստուգում", "pro": "Անսահմանափակ Pro", "price_9": "9", "price_29": "29",
        "buy": "Գնել", "upload": "Վերբեռնել PDF պայմանագիրը", "demo_tab": "📝 Օրինակ",
        "main_tab": "🚀 AI Վերլուծություն", "risk_label": "Իրավաբանական ռիսկի գնահատական.",
        "btn_run": "Սկսել վերլուծությունը", "wait_msg": "Վերբեռնեք փաստաթուղթը...",
        "pay_to_unlock": "🔒 Վճարեք {price} {cur} ամբողջական հաշվետվության համար:",
        "demo_content": "🔴 **Կրիտիկական ռիսկ.** Գնի փոփոխություն առանց ծանուցման:\n\n🟠 **Միջին ռիսկ.** Պայմանագրի դադարեցման անորոշ պայմաններ:\n\n✅ **Եզրակացություն.** Բարձր ռիսկ: Մի ստորագրեք առանց լրացուցիչ ստուգման:"
    }
}

# --- 6. ИНТЕРФЕЙС ---
# Выбор языка (стилизованный)
st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
lang_choice = st.radio("", ["English", "Русский", "Հայերեն"], horizontal=True, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)
t = translations[lang_choice]

# Заголовок
st.markdown(f"<h1 style='text-align: center;'>⚖️ JurisClear AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>{t['subtitle']}</p>", unsafe_allow_html=True)
st.divider()

# Тарифы (Колонки)
c1, c2 = st.columns(2)
with c1:
    st.info(f"### {t['one_time']}\n## {t['price_9']} {t['cur']}")
    st.link_button(t['buy'], LINK_9USD)
with c2:
    st.success(f"### {t['pro']}\n## {t['price_29']} {t['cur']} {t['mo']}")
    st.link_button(t['buy'], LINK_29USD)

st.write("") # Отступ

# Вкладки
tab1, tab2 = st.tabs([t['main_tab'], t['demo_tab']])

with tab1:
    uploaded_file = st.file_uploader(t['upload'], type="pdf")
    if uploaded_file:
        if st.button(t['btn_run'], type="primary"):
            with st.spinner("AI analyzing document..."):
                # Чтение PDF
                reader = PdfReader(uploaded_file)
                text = "".join([page.extract_text() for page in reader.pages])
                
                # Получение анализа
                report = get_ai_analysis(text, lang_choice)
                
                st.subheader(t['risk_label'])
                st.markdown(report)
                st.divider()
                
                # Призыв к оплате после превью
                st.warning(t['pay_to_unlock'].format(price=t['price_9'], cur=t['cur']))
                st.link_button(f"👉 {t['buy']} ({t['price_9']} {t['cur']})", LINK_9USD)
    else:
        st.info(t['wait_msg'])

with tab2:
    st.markdown(f"### {t['demo_tab']}")
    st.markdown(t['demo_content'])

# --- 7. ФУТЕР (Контакты для солидности) ---
st.write("")
st.divider()
f1, f2, f3 = st.columns(3)
with f1:
    st.caption("JurisClear AI © 2026")
with f2:
    st.caption("Contact: support@jurisclear.com")
with f3:
    st.caption("Yerevan, Armenia")
