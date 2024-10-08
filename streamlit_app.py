import streamlit as st
import openai
from parse_hh import extract_candidate_data, get_html

import streamlit as st

# Проверяем наличие ключа в st.secrets
if "api_key" in st.secrets:
    api_key = st.secrets["api_key"]
else:
    # Запрашиваем ключ у пользователя
    api_key = st.text_input("Введите ваш OpenAI API ключ:", type="password")
    



# Создаем клиента OpenAI
client = openai.Client(api_key=api_key)


def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # Укажите нужную вам модель, например, "gpt-4"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0
    ) 

    return response.choices[0].message.content


st.title('Оценка резюме на хедхантере')

job_description = st.text_area('Описание вашей вакансии в текстовом виде')

cv =  st.text_area('Резюме кандидата в текстовом виде (или можно поставить ниже ссылку на резюме)')
cv_url = st.text_input('Ссылка на резюме на HH.ru')

if cv:
    cv = cv
elif cv_url:
    cv = extract_candidate_data(get_html(cv_url).text)
    st.write(cv)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.

При выводе результатов используй markdown
""".strip()

if st.button('Оценить'):
    with st.spinner('Ждем оценки...'):
        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
        response = request_gpt(SYSTEM_PROMPT, user_prompt)

    st.write(response)
