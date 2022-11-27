import requests
from itertools import count

from predict_salary import predict_rub_salary


def get_sj_vacancies(sj_key, page=0, language='Python', profession_id=48, town_id=4, period=30):
    sj_url = "https://api.superjob.ru/2.0/vacancies"
    headers = {
        'X-Api-App-Id': sj_key
    }
    params = {
        'catalogues': profession_id,
        'town': town_id,
        'period': period,
        'page': page,
        'keyword': language
    }
    response = requests.get(sj_url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_sj_vacancies_statistics(sj_key, language="Python"):
    average_salaries = []
    for page in count(0, 1):
        vacancies = get_sj_vacancies(
            sj_key,
            page,
            language=language
        )
        for vacancy in vacancies["objects"]:
            if not vacancy["payment_from"] and not vacancy["payment_to"] or vacancy["currency"] != "rub":
                continue
            salary = predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"])
            average_salaries.append(salary)
        if not vacancies["more"]:
            break
    vacancies_processed = len(average_salaries)
    if not vacancies_processed:
        average_salary = 0
    else:
        average_salary = sum(average_salaries) // vacancies_processed
    about_programming_vacancies = {
        "vacancies_found": vacancies["total"],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return about_programming_vacancies


def get_sj_vacancies_languages_statistics(sj_key):
    sj_programming_languages = ["Python", "Java", "JavaScript", "Ruby", "PHP", "C++", "C#", "C", "Go", "1C"]
    sj_salary_statistics = {}
    for language in sj_programming_languages:
        sj_salary_statistics[language] = get_sj_vacancies_statistics(sj_key, language)
    return sj_salary_statistics
