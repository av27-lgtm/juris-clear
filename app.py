import streamlit as st
import openai
import PyPDF2

# Настройка внешнего вида страницы
st.set_page_config(page_title="JurisClear AI - Твой юридический аудитор", page_icon="⚖️")

st.title("⚖️ JurisClear AI")
st.subheader("Мгновенный анализ юридических рисков")

# Поле для API-ключа (в будущем мы его спрячем, но для теста пока так)
api_key = st.sidebar.text_input("Введите ваш OpenAI API Key", type="password")

# Инструкция для пользователя
st.write("Загрузите ваш договор в формате PDF, и ИИ проанализирует его на наличие скрытых угроз.")

uploaded_file = st.file_uploader("Выбрать файл договора (PDF)", type="pdf")

if uploaded_file is not None and api_key:
    openai.api_key = api_key
    
    # Читаем текст из PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    contract_text = ""
    for page in pdf_reader.pages:
        contract_text += page.extract_text()

    if st.button("Начать юридический аудит"):
        with st.spinner('Профессиональный юрист ИИ изучает документ...'):
            try:
                # Отправляем запрос в OpenAI
                response = openai.chat.completions.create(
                    model="gpt-4o", # Самая мощная модель
                    messages=[
                        {"role": "system", "content": "Ты — опытный юрист. Твоя задача: проанализировать договор, выделить 3 главных риска для клиента, объяснить сложные моменты простым языком и дать рекомендации по изменению текста."},
                        {"role": "user", "content": f"Проанализируй этот текст договора:\n\n{contract_text}"}
                    ]
                )
                
                analysis = response.choices[0].message.content
                
                st.success("Анализ завершен!")
                st.markdown("### Результаты аудита:")
                st.write(analysis)
                
                st.warning("Внимание: Это автоматический анализ. Всегда консультируйтесь с живым юристом для принятия финальных решений.")
                
            except Exception as e:
                st.error(f"Произошла ошибка: {e}. Проверьте баланс вашего API ключа.")

elif not api_key:
    st.info("Пожалуйста, введите ваш API ключ в боковой панели, чтобы начать работу.")
