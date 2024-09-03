import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата с проверкой на None
    name_element = soup.find('h2', {'data-qa': 'bloko-header-1'})
    name = name_element.text.strip() if name_element else "Имя не указано"

    gender_age_element = soup.find('p')
    gender_age = gender_age_element.text.strip() if gender_age_element else "Пол и возраст не указаны"

    location_element = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location_element.text.strip() if location_element else "Местоположение не указано"

    job_title_element = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title_element.text.strip() if job_title_element else "Должность не указана"

    job_status_element = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status_element.text.strip() if job_status_element else "Статус не указан"

    # Извлечение опыта работы с проверкой на None
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experiences = []
    if experience_section:
        experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
        for item in experience_items:
            period_element = item.find('div', class_='bloko-column_s-2')
            period = period_element.text.strip() if period_element else "Период работы не указан"

            duration_element = item.find('div', class_='bloko-text')
            duration = duration_element.text.strip() if duration_element else ""

            period = period.replace(duration, f" ({duration})") if duration else period

            company_element = item.find('div', class_='bloko-text_strong')
            company = company_element.text.strip() if company_element else "Компания не указана"

            position_element = item.find('div', {'data-qa': 'resume-block-experience-position'})
            position = position_element.text.strip() if position_element else "Должность не указана"

            description_element = item.find('div', {'data-qa': 'resume-block-experience-description'})
            description = description_element.text.strip() if description_element else "Описание не указано"

            experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

    # Извлечение ключевых навыков с проверкой на None
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else []

    # Формирование строки в формате Markdown
    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown

# Пример использования:
response = get_html('https://nn.hh.ru/resume/9a414dcf000220a3030039ed1f4c5350344854?query=prompt+engineer&searchRid=17253567346887ff7fdf8a9dafbfbd36&hhtmFrom=resume_search_result')
print(extract_candidate_data(response.text))
# Пишем HTML в файл с указанием кодировки utf-8
with open("vacancy.html", "w", encoding="utf-8") as f:
    f.write(response.text)
