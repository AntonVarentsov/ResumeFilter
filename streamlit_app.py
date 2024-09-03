import streamlit as st
import openai
from parse_hh import extract_candidate_data, get_html

api_key = st.secrets["api_key"]

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


st.title('CV Scoring App')

job_description = st.text_area('Job Description')

cv =  st.text_area('CV')
cv_url = st.text_input('CV URL')

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

if st.button('Score'):
    with st.spinner('Wait for it...'):
        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
        response = request_gpt(SYSTEM_PROMPT, user_prompt)

    st.write(response)
