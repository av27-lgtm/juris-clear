import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import re

# --- 1. CONFIG (ТЕХНИЧЕСКАЯ ЧАСТЬ) ---
st.set_page_config(
    page_title="JurisClear AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ПОЛНЫЙ CSS ИНТЕРФЕЙСА ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 1.5rem; max-width: 1000px;}
    
    /* Тарифные планы */
    .pricing-card-single {
        background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
        padding: 20px; border-radius: 15px; border: 1px solid #60a5fa; text-align: center; color: white;
    }
    .pricing-card-pro {
        background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
        padding: 20px; border-radius: 15px; border: 1px solid #34d399; text-align: center; color: white;
    }
    
    /* Карточка отчета */
    .report-card {
        background-color: #1e293b; border-left: 5px solid #3b82f6;
        padding: 25px; border-radius: 12px; margin-top: 20px; color: #f1f5f9;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }
    
    /* ОБЪЕМНЫЙ КОНТЕЙНЕР ДЛЯ ШКАЛЫ */
    .risk-meter-container {
        background: #0f172a; border-radius: 15px; padding: 8px;
        box-shadow: inset 0 3px 8px rgba(0,0,0,0.6); border: 1px solid #334155; margin: 15px 0;
    }
    
    .stButton>button {
        border-radius: 12px; height: 3.8em; font-weight: bold; transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ЛОГИКА ДИНАМИЧЕСКОЙ ШКАЛЫ ---
def get_risk_params(score):
    if score <= 3: # Низкий
        return "linear-gradient(90deg, #059669 0%, #10b981 100%)", "rgba(16, 185, 129, 0.5)", "LOW"
    elif score <= 6: # Средний
        return "linear-gradient(90deg, #d97706 0%, #fbbf24 100%)", "rgba(251, 191, 36, 0.5)", "MEDIUM"
    else: # Высокий
        return "linear-gradient(90deg, #dc2626 0%, #ef4444 100%)", "rgba(239, 68, 68, 0.5)", "CRITICAL"

# --- 4. ИНИЦИАЛИЗАЦИЯ И ПРИМЕРЫ ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

sample_en = "### Summary: Software Agreement\n1. **IP Risk:** Background code ownership is unclear.\n2. **Termination:** 90-day notice is excessive.\n3. **Liability:** Capped too low ($500)."
sample_ru = "### Резюме: Договор услуг\n1. **Цена:** Право менять стоимость в одностороннем порядке.\n2. **Штрафы:** 1% в день — это кабальные условия.\n3. **Суд:** Только по месту регистрации Исполнителя."
sample_hy = "### Ամփոփում. Ծառայությունների պայմանագիր\n1. **Գաղտնիություն:** Ժամկետները նշված չեն:\n2. **Տուժանք:** 0.5% օրական, ինչը բարձր է:\n3. **Լուծարում:** Առանց նախնական ծանուցման:"

# --- 5. ТРАНСЛЯЦИИ ---
translations = {
    "English": {
        "cur": "$", "p9": "9", "p29": "29", "mo": "/mo",
        "one_time": "Single Audit", "pro": "Unlimited Pro",
        "buy": "Get Full Access", "upload": "Drag and drop PDF contract",
        "btn_run": "Run AI Analysis", "main_tab": "🚀 AI Audit", "demo_tab": "📝 See Demo",
        "risk_label": "Dynamic AI Risk Score:", "wait": "Awaiting document...",
        "pay_msg": "🔒 Unlock full remediation plan for {p}{c}",
        "prompt": "Analyze this contract. List 3 risks. End with 'SCORE: X' (X=1-10). Language: English.",
        "sample": sample_en
    },
    "Русский": {
        "cur": "₽", "p9": "850", "p29": "2500", "mo": "/мес",
        "one_time": "Разовый аудит", "pro": "Безлимит Pro",
        "buy": "Купить доступ", "upload": "Загрузите PDF договор",
        "btn_run": "Начать анализ", "main_tab": "🚀 ИИ Аудит", "demo_tab": "📝 Пример отчета",
        "risk_label": "ИИ Оценка Риска:", "wait": "Загрузите файл...",
        "pay_msg": "🔒 Открыть план устранения рисков за {p} {c}",
        "prompt": "Проанализируй договор. 3 риска. В конце напиши 'SCORE: X' (X=1-10). Язык: Русский.",
        "sample": sample_ru
    },
    "Հայերեն": {
        "cur": "֏", "p9": "3500", "p29": "11000", "mo": "/ամիս",
        "one_time": "Մեկանգամյա", "pro": "Անսահմանափակ Pro",
        "buy": "Գնել", "upload": "Վերբեռնել PDF",
        "btn_run": "Սկսել", "main_tab": "🚀 AI Աուդիտ", "demo_tab": "📝 Օրինակ",
        "risk_label": "AI Ռիսկի ցուցանիշ.", "wait": "Վերբեռնեք ֆայլը...",
        "pay_msg": "🔒 Բացել ամբողջական վերլուծությունը {p} {c}-ով",
        "prompt": "Վերլուծիր պայմանագիրը: 3 ռիսկ: Վերջում գրիր 'SCORE: X' (X=1-10): Լեզուն՝ հայերեն:",
        "sample": sample_hy
    }
}

# --- 6. ИНТЕРФЕЙС ---
c_lang, _ = st.columns([1, 2])
with c_lang:
    lang = st.selectbox("", ["English", "Русский", "Հայերեն"], label_visibility="collapsed")
t = translations[lang]

st.markdown(f"<h1 style='text-align: center; color: white;'>⚖️ JurisClear <span style='color:#3b82f6'>AI</span></h1>", unsafe_allow_html=True)

# Тарифы
col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"<div class='pricing-card-single'><h3>{t['one_time']}</h3><h2>{t['p9']} {t['cur']}</h2></div>", unsafe_allow_html=True)
    st.write("")
    st.link_button(t['buy'], "https://jurisclear.lemonsqueezy.com/...", use_container_width=True)
with col_b:
    st.markdown(f"<div class='pricing-card-pro'><h3>{t['pro']}</h3><h2>{t['p29']} {t['cur']} <small>{t['mo']}</small></h2></div>", unsafe_allow_html=True)
    st.write("")
    st.link_button(t['buy'], "https://jurisclear.lemonsqueezy.com/...", use_container_width=True)

st.divider()

# Вкладки
tab_audit, tab_demo = st.tabs([t['main_tab'], t['demo_tab']])

with tab_audit:
    file = st.file_uploader(t['upload'], type="pdf", label_visibility="collapsed")
    if file:
        if st.button(t['btn_run'], use_container_width=True, type="primary"):
            with st.spinner("AI Analysis..."):
                reader = PdfReader(file)
                text = "".join([p.extract_text() for p in reader.pages])
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"{t['prompt']}\n\n{text[:4000]}"}]
                )
                raw_res = response.choices[0].message.content
                
                # Парсинг счета
                score_match = re.search(r"SCORE:\s*(\d+)", raw_res)
                score = int(score_match.group(1)) if score_match else 5
                clean_res = raw_res.replace(f"SCORE: {score}", "").strip()
                
                # Рендер шкалы
                bar_color, bar_shadow, risk_text = get_risk_params(score)
                st.write(f"### {t['risk_label']}")
                st.markdown(f"""
                    <div class="risk-meter-container">
                        <div style="height:35px; width:{score*10}%; background:{bar_color}; 
                        box-shadow: 0 4px 15px {bar_shadow}; border-radius:10px; 
                        display:flex; align-items:center; justify-content:center; color:white; font-weight:900;">
                            {risk_text} ({score}/10)
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<div class='report-card'>{clean_res}</div>", unsafe_allow_html=True)
                st.warning(t['pay_msg'].format(p=t['p9'], c=t['cur']))
    else:
        st.info(t['wait'])

with tab_demo:
    # Статичный пример для демо
    bar_color, bar_shadow, risk_text = get_risk_params(9)
    st.write(f"### {t['risk_label']}")
    st.markdown(f"""
        <div class="risk-meter-container">
            <div style="height:35px; width:90%; background:{bar_color}; 
            box-shadow: 0 4px 15px {bar_shadow}; border-radius:10px; 
            display:flex; align-items:center; justify-content:center; color:white; font-weight:900;">
                CRITICAL (9/10)
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='report-card'>{t['sample']}</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 JurisClear AI | Yerevan | support@jurisclear.com")
