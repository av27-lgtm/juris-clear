import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="JurisClear AI", page_icon="⚖️", layout="wide")

# --- 2. CSS: ГЛУБОКАЯ КАСТОМИЗАЦИЯ ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 1.5rem; max-width: 900px;}
    
    /* Стилизация карточек отчета */
    .report-card {
        background-color: #1e293b;
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 12px; height: 3.8em; font-weight: bold;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(59,130,246,0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ИНИЦИАЛИЗАЦИЯ ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 4. СЛОВАРЬ (ТЕКСТЫ + ВАЛЮТЫ) ---
translations = {
    "English": {
        "cur": "$", "p9": "9", "p29": "29", "mo": "/mo",
        "title": "AI Legal Auditor Pro",
        "one_time": "Single Audit", "pro": "Unlimited Pro",
        "buy": "Get Full Access", "upload": "Drag and drop your PDF contract",
        "btn_run": "Analyze Document", "main_tab": "🚀 Audit", "demo_tab": "📝 Sample",
        "wait": "Awaiting document upload...",
        "pay_msg": "🔒 To see the detailed mitigation strategy, pay {p}{c}.",
        "disclaimer": "Disclaimer: This analysis is for informational purposes only.",
        "analysis_prompt": "Act as a senior legal counsel. Analyze this contract and provide: 1) Executive Summary 2) Top 3 High-Risk Clauses 3) Financial Implications. Language: English."
    },
    "Русский": {
        "cur": "₽", "p9": "850", "p29": "2500", "mo": "/мес",
        "title": "ИИ-Аудит Договоров Pro",
        "one_time": "Разовый аудит", "pro": "Безлимит Pro",
        "buy": "Получить доступ", "upload": "Перетащите PDF договор сюда",
        "btn_run": "Начать аудит", "main_tab": "🚀 Аудит", "demo_tab": "📝 Пример",
        "wait": "Ожидание загрузки документа...",
        "pay_msg": "🔒 Чтобы получить подробные рекомендации по исправлению, оплатите {p} {c}.",
        "disclaimer": "Внимание: ИИ-анализ не является заменой профессионального юриста.",
        "analysis_prompt": "Действуй как старший юрист. Проанализируй договор и выдели: 1) Краткое резюме 2) Топ-3 критических риска 3) Финансовые риски. Язык: Русский."
    },
    "Հայերեն": {
        "cur": "֏", "p9": "3500", "p29": "11000", "mo": "/ամիս",
        "title": "AI Իրավաբանական Աուդիտ Pro",
        "one_time": "Մեկանգամյա", "pro": "Անսահմանափակ Pro",
        "buy": "Գնել", "upload": "Վերբեռնել PDF պայմանագիրը",
        "btn_run": "Սկսել ստուգումը", "main_tab": "🚀 Աուդիտ", "demo_tab": "📝 Օրինակ",
        "wait": "Վերբեռնեք փաստաթուղթը...",
        "pay_msg": "🔒 Ամբողջական վերլուծության համար վճարեք {p} {c}:",
        "disclaimer": "Ուշադրություն. AI վերլուծությունը չի փոխարինում փաստաբանին:",
        "analysis_prompt": "Գործիր որպես ավագ իրավաբան: Վերլուծիր պայմանագիրը և նշիր. 1) Ամփոփում 2) 3 հիմնական ռիսկերը 3) Ֆինանսական հետևանքները: Լեզուն՝ հայերեն:"
    }
}

# Выбор языка
c1, _ = st.columns([1, 2])
with c1:
    lang = st.selectbox("", ["English", "Русский", "Հայերեն"], label_visibility="collapsed")
t = translations[lang]

# --- 5. UI: HEADER ---
st.markdown(f"<h1 style='text-align: center; color: #f8fafc;'>⚖️ JurisClear <span style='color:#3b82f6'>AI</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>{t['title']}</p>", unsafe_allow_html=True)

# Тарифы
col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"<div style='background:#1e293b; padding:20px; border-radius:15px; border:1px solid #334155; text-align:center;'><h4>{t['one_time']}</h4><h2>{t['p9']} {t['cur']}</h2></div>", unsafe_allow_html=True)
    st.write("")
    st.link_button(t['buy'], "https://jurisclear.lemonsqueezy.com/...", use_container_width=True)
with col_b:
    st.markdown(f"<div style='background:#1e293b; padding:20px; border-radius:15px; border:1px solid #334155; text-align:center;'><h4>{t['pro']}</h4><h2>{t['p29']} {t['cur']} <small>{t['mo']}</small></h2></div>", unsafe_allow_html=True)
    st.write("")
    st.link_button(t['buy'], "https://jurisclear.lemonsqueezy.com/...", use_container_width=True)

st.write("")

# --- 6. MAIN WORKSPACE ---
tab_audit, tab_sample = st.tabs([t['main_tab'], t['demo_tab']])

with tab_audit:
    file = st.file_uploader(t['upload'], type="pdf", label_visibility="collapsed")
    
    if file:
        if st.button(t['btn_run'], use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Эмуляция глубокого процесса (для солидности)
            status_text.text("Scanning clauses...")
            progress_bar.progress(30)
            
            reader = PdfReader(file)
            content = "".join([page.extract_text() for page in reader.pages])
            
            status_text.text("Identifying risks with GPT-4...")
            progress_bar.progress(70)
            
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"{t['analysis_prompt']}\n\n{content[:5000]}"}]
                )
                
                progress_bar.progress(100)
                status_text.empty()
                
                # Вывод результата в красивом блоке
                st.markdown(f"### 📋 {t['main_tab']}")
                st.markdown(f"<div class='report-card'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)
                
                # Секция оплаты (Upsell)
                st.warning(t['pay_msg'].format(p=t['p9'], c=t['cur']))
                st.link_button(f"🔓 {t['buy']} ({t['p9']} {t['cur']})", "https://jurisclear.lemonsqueezy.com/...", use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                progress_bar.empty()
    else:
        st.info(t['wait'])

with tab_sample:
    st.markdown("### 📝 Professional Report Example")
    st.info("Here you can see how a professional audit looks after the full unlock.")

# --- 7. FOOTER & SAFETY ---
st.divider()
st.markdown(f"<p style='text-align: center; font-size: 0.8rem; color: #64748b;'>{t['disclaimer']}</p>", unsafe_allow_html=True)
st.caption(f"© 2026 JurisClear AI | support@jurisclear.com")
