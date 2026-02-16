import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

# --- 1. ТВОИ НАСТРОЙКИ ---
LINK_9USD = "https://jurisclearai.lemonsqueezy.com/checkout/buy/a06e3832-bc7a-4d2c-8f1e-113446b2bf61"
LINK_29USD = "https://jurisclearai.lemonsqueezy.com/checkout/buy/69a180c9-d5f5-4018-9dbe-b8ac64e4ced8"

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Check OpenAI API Key in Secrets")

# --- 2. ЛОГИКА ИИ ---
def get_ai_analysis(text, lang):
    # Улучшенный промпт для точности
    prompts = {
        "Русский": "Ты эксперт-юрист. Проанализируй текст договора и найди 3 главных риска. Отвечай строго на русском.",
        "English": "You are a legal expert. Analyze the contract text and find 3 main risks. Answer strictly in English.",
        "Հայերեն": "Դուք իրավաբանական փորձագետ եք: Վերլուծեք պայմանագրի տեքստը և գտեք 3 հիմնական ռիսկ: Պատասխանեք խստորեն հայերեն:"
    }
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You provide professional legal risk assessments."},
                {"role": "user", "content": f"{prompts[lang]}\n\nText:\n{text[:4000]}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- 3. СЛОВАРЬ (Теперь с переводом Примеров) ---
translations = {
    "English": {
        "cur": "$", "mo": "/ mo", "title": "JurisClear AI", "subtitle": "Legal Document Audit",
        "buy": "Unlock Full Analysis", "upload": "Upload PDF", "demo_tab": "📝 Sample Report",
        "main_tab": "🚀 Analysis", "btn_run": "Start Analysis",
        "sample_text": "🔴 **Critical Risk:** Clause 4.2 allows rent increase without notice."
    },
    "Русский": {
        "cur": "₽", "mo": "/ мес.", "title": "JurisClear AI", "subtitle": "Юридический аудит",
        "buy": "Открыть полный отчет", "upload": "Загрузить PDF", "demo_tab": "📝 Пример отчета",
        "main_tab": "🚀 Анализ", "btn_run": "Начать анализ",
        "sample_text": "🔴 **Критический риск:** Пункт 4.2 позволяет повышать цену без уведомления."
    },
    "Հայերեն": {
        "cur": "֏", "mo": "/ ամիս", "title": "JurisClear AI", "subtitle": "Իրավաբանական աուդիտ",
        "buy": "Բացել հաշվետվությունը", "upload": "Վերբեռնել PDF", "demo_tab": "📝 Օրինակ",
        "main_tab": "🚀 Վերլուծություն", "btn_run": "Սկսել վերլուծությունը",
        "sample_text": "🔴 **Կրիտիկական ռիսկ.** 4.2 կետը թույլ է տալիս բարձրացնել գինը առանց ծանուցման:"
    }
}

st.set_page_config(page_title="JurisClear AI", layout="wide")

# Язык
lang_choice = st.sidebar.radio("Language / Язык / Լեզու", ["Русский", "English", "Հայերեն"])
t = translations[lang_choice]

st.title(f"⚖️ {t['title']}")
st.caption(t['subtitle'])

# Тарифы (вставим твои ссылки)
c1, c2 = st.columns(2)
with c1:
    st.info(f"9 {t['cur']}")
    st.link_button(t['buy'], LINK_9USD, use_container_width=True)
with c2:
    st.success(f"29 {t['cur']} {t['mo']}")
    st.link_button(t['buy'], LINK_29USD, use_container_width=True)

# Вкладки
tab1, tab2 = st.tabs([t['main_tab'], t['demo_tab']])

with tab1:
    file = st.file_uploader(t['upload'], type="pdf")
    if file:
        if st.button(t['btn_run']):
            reader = PdfReader(file)
            text = "".join([p.extract_text() for p in reader.pages])
            res = get_ai_analysis(text, lang_choice)
            st.markdown(res)
            st.link_button(f"👉 {t['buy']}", LINK_9USD)

with tab2:
    st.markdown(f"### {t['demo_tab']}")
    st.info(t['sample_text']) # ТЕПЕРЬ ОНО ПЕРЕВОДИТСЯ!
